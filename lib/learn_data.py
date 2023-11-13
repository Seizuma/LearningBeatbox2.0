from config.config import *
import scipy
import scipy.io.wavfile
import os
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import cross_val_score, train_test_split
import joblib
import time
import warnings
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy.fftpack import fft, rfft, fft2, dct
from python_speech_features import mfcc
from sklearn.manifold import TSNE
from sklearn import preprocessing
from lib.machinelearning import *
from sklearn.neural_network import *
from lib.combine_models import define_settings, get_current_default_settings
from lib.audio_model import AudioModel
from lib.wav import load_wav_files_with_srts

def learn_data():
    dir_path = os.path.join( os.path.dirname( os.path.dirname( os.path.realpath(__file__)) ), DATASET_FOLDER)    
    data_directory_names = [directory for directory in os.listdir( dir_path ) if os.path.isdir(dir_path + "/" + directory)]
    
    print( "-------------------------" )
    if (len(data_directory_names) < 2):
        print("You haven't recorded enough different sounds yet in " + DATASET_FOLDER + "! Make sure to record at least two different sounds before you train a model")
        print( "-------------------------" )
        return
    else:
        print( "Time to learn the audio files")
        print( "This script is going to analyze all your generated audio snippets" )
        print( "And attempt to learn the sounds to their folder names" )
        print( "-------------------------" )
    
    settings = define_settings(get_current_default_settings())
    
    clf_filename = input("Insert the model name ( empty is '" + DEFAULT_CLF_FILE + "' ) ")
    if( clf_filename == "" ):
        clf_filename = DEFAULT_CLF_FILE
    clf_filename += '.pkl'
    
    print( "Type the algorithm that you wish to use for recognition")
    print( "- [R] Random Forest ( SKLEARN - For quick verification )" )
    if( PYTORCH_AVAILABLE ):
        print( "- [A] Audio Net ( Neural net in Pytorch - Required by TalonVoice )" )
    print( "- [M] Multi Layer Perceptron ( Neural net in SKLEARN )" )
    print( "- [X] Exit the learning" )

    
    model_type = input("")
    while model_type == "":
        model_type = input("")

    if( model_type.lower() == "r" ):
        classifier = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=123)
        print( "Selected random forest!")        
        
        fit_sklearn_classifier( classifier, dir_path, clf_filename, settings )        
    elif( model_type.lower() == "m" ):
        classifier = MLPClassifier(activation='relu', early_stopping=True,
              epsilon=1e-08, hidden_layer_sizes=(1024, 1024, 1024, 512),
              learning_rate='constant', learning_rate_init=0.001,
              max_iter=1000, momentum=0.9,
              nesterovs_momentum=True, power_t=0.5, random_state=1,
              shuffle=True, solver='adam', tol=0.0001,
              validation_fraction=0.1, verbose=True, warm_start=False)
        print( "Selected multi layer perceptron!")
        
        fit_sklearn_classifier( classifier, dir_path, clf_filename, settings )
    elif( model_type.lower() == "x" ):
        return
    elif( model_type.lower() == "a" and PYTORCH_AVAILABLE ):
        print( "Selected Audio Net!")
        print( "How many nets do you wish to train at the same time? ( Default is 3 )" )
        net_count = input("")
        if ( net_count == "" ):
            net_count = 3
        else:
            net_count = int(net_count)

        # Import pytorch related thins here to make sure pytorch isn't a hard requirement
        from lib.audio_net import AudioNetTrainer
        from lib.audio_dataset import AudioDataset
        
        print( "--------------------------" )        
        dataset_labels = determine_labels( dir_path )
        print( "--------------------------" )
        grouped_data_directories =  get_grouped_data_directories( dataset_labels )
        dataset = AudioDataset( grouped_data_directories, settings )
        trainer = AudioNetTrainer(dataset, net_count, settings)
        
        print( "Learning the data..." )
        trainer.train( clf_filename )

def fit_sklearn_classifier( classifier,  dir_path, clf_filename, settings ):
    max_files_per_category = input("How many files should we analyze per category? ( empty is all )" )
    if( max_files_per_category == "" ):
        max_files_per_category = 1000000
    else:
        max_files_per_category = int( max_files_per_category )
    
    print( "--------------------------" )
    dataX, dataY, directory_names, total_feature_engineering_time = load_data( dir_path, max_files_per_category, settings['FEATURE_ENGINEERING_TYPE'] )
    print( "--------------------------" )

    print( "Learning the data..." )
    classifier.fit( dataX, dataY )
    print( "Data analyzed!               " )
    
    print( "Testing algorithm speed... ", end="\r" )
    feature_engineering_speed_ms = int(total_feature_engineering_time) / len( dataX )
    prediction_speed_ms = average_prediction_speed( classifier, dataX )
    print( "Worst case reaction speed: +- %0.4f milliseconds " % ( feature_engineering_speed_ms + prediction_speed_ms + ( RECORD_SECONDS * 1000 ) ) )
    print( "- Preparing data speed %0.4f ms " % feature_engineering_speed_ms )
    print( "- Predicting label speed %0.4f ms" % prediction_speed_ms )
    print( "- Recording length %0.4f ms" % ( RECORD_SECONDS * 1000 ) )
    
    persisted_classifier = AudioModel( settings, classifier )
    
    print( "Saving the model to " + CLASSIFIER_FOLDER + "/" + clf_filename )
    joblib.dump( persisted_classifier, CLASSIFIER_FOLDER + "/" + clf_filename )
    print( "--------------------------" )
    
    if ( not isinstance(classifier, MLPClassifier ) ):
        print( "Predicting recognition accuracy using cross validation...", end="\r" )
        scores = cross_validation( classifier, dataX, dataY )
        print( "Accuracy: %0.4f (+/- %0.4f)                               " % (scores.mean(), scores.std() * 2))
    
    detailed_analysis = input("Should we do a detailed analysis of the model? Y/n" ).lower() == 'y'
    if( detailed_analysis ):
        create_confusion_matrix( classifier, dataX, dataY, directory_names )
        print( "--------------------------" )
    
    
def load_wav_files( directories, label, int_label, start, end, input_type ):
    category_dataset_x = []
    category_dataset_labels = []
    totalFeatureEngineeringTime = 0
    category_file_index = 0

    for directory in directories:
        for fileindex, file in enumerate(os.listdir(directory)):
            if ( file.endswith(".wav") and fileindex >= start and len(category_dataset_x) < end ):
                full_filename = os.path.join(directory, file)
                print( "Loading " + str(category_file_index) + " files for " + label + "... ", end="\r" )
                category_file_index += 1

                # Load the WAV file and turn it into a onedimensional array of numbers
                feature_engineering_start = time.time() * 1000
                data_row, frequency = feature_engineering( full_filename, RECORD_SECONDS, input_type )
                category_dataset_x.append( data_row )
                category_dataset_labels.append( label )
                totalFeatureEngineeringTime += time.time() * 1000 - feature_engineering_start

    print( "Loaded " + str( len( category_dataset_labels ) ) + " .wav files for category " + label + " (id: " + str(int_label) + ")" )
    return category_dataset_x, category_dataset_labels, totalFeatureEngineeringTime

def determine_labels( dir_path ):
    data_directory_names =  [directory for directory in os.listdir( dir_path ) if not directory.startswith(".")]
    
    print( "Selecting categories to train on... ( [Y]es / [N]o / [S]kip )" )
    filtered_data_directory_names = []
    for directory_name in data_directory_names:
        add = input(" - " + directory_name)
        if( add == "" or add.strip().lower() == "y" ):
            filtered_data_directory_names.append( directory_name )
        elif( add.strip().lower() == "s" ):
            break
        else:
            print( "Disabled " + directory_name )

    return filtered_data_directory_names

def get_grouped_data_directories( labels ):
    # If the microphone separator setting is set use that to split directory names into categories/labels.
    # This enable us to have multiple directories with different names and as long as they have the same prefix they will be combined into a single category/label.
    grouped_data_directories = {}
    for directory_name in labels:
        if MICROPHONE_SEPARATOR:
            category_name = directory_name.split( MICROPHONE_SEPARATOR )[0] 
        else:
            category_name = directory_name
        if category_name not in grouped_data_directories:
            grouped_data_directories[ category_name ] = []
        data_directory = f"{ DATASET_FOLDER }/{ directory_name.lower() }"
        grouped_data_directories[ category_name ].append( data_directory )
    return grouped_data_directories

def load_data( dir_path, max_files, input_type ):
    filtered_data_directory_names = determine_labels( dir_path )
    grouped_data_directories =  get_grouped_data_directories( filtered_data_directory_names )

    # Generate the training set and labels with them
    dataset = []
    dataset_x = []
    dataset_labels = []

    totalFeatureEngineeringTime = 0
    for str_label, directories in grouped_data_directories.items():
        # Add a label used for classifying the sounds
        id_label = get_label_for_directory( "".join( directories ) )
        cat_dataset_x, cat_dataset_labels, featureEngineeringTime = load_wav_files_with_srts( directories, str_label, id_label, 0, max_files, input_type )
        totalFeatureEngineeringTime += featureEngineeringTime
        dataset_x.extend( cat_dataset_x )
        dataset_labels.extend( cat_dataset_labels )

    return dataset_x, dataset_labels, grouped_data_directories.keys(), totalFeatureEngineeringTime

