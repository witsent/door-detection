#Model training


##For create samples:
`use opencv_createsamples -vec <name>.vec -info <path to marking file> -w <width> -h <height> -num <number of positive data>`

###Example:
`opencv_createsamples -vec doors.vec -info ../dataset/door.idx -w 30 -h 69 -num 255`


##For model training:
There are two applications in OpenCV to train cascade classifier: opencv_haartraining and opencv_traincascade. opencv_traincascade is a newer version, written in C++ in accordance to OpenCV 2.x API. But the main difference between this two applications is that opencv_traincascade supports both Haar and Local Binary Patterns features. LBP features are integer in contrast to Haar features, so both training and detection with LBP are several times faster then with Haar features. Regarding the LBP and Haar detection quality, it depends on training: the quality of training dataset first of all and training parameters too. It's possible to train a LBP-based classifier that will provide almost the same quality as Haar-based one.

`opencv_traincascade`  
> -data <cascade_dir_name>  
> -vec <vec_file_name>  
> -bg <background_file_name>  
> [-numPos <number_of_positive_samples = 2000>]  
> [-numNeg <number_of_negative_samples = 1000>]  
> [-numStages <number_of_stages = 20>]  
> [-precalcValBufSize <precalculated_vals_buffer_size_in_Mb = 1024>]  
> [-precalcIdxBufSize <precalculated_idxs_buffer_size_in_Mb = 1024>]  
> [-baseFormatSave]  
> [-numThreads <max_number_of_threads = 9>]  
> [-acceptanceRatioBreakValue <value> = -1>]  
>--cascadeParams--  
> [-stageType <BOOST(default)>]  
> [-featureType <{HAAR(default), LBP, HOG}>]  
> [-w <sampleWidth = 24>]  
> [-h <sampleHeight = 24>]  
>--boostParams--  
> [-bt <{DAB, RAB, LB, GAB(default)}>]  
> [-minHitRate <min_hit_rate> = 0.995>]  
> [-maxFalseAlarmRate <max_false_alarm_rate = 0.5>]  
> [-weightTrimRate <weight_trim_rate = 0.95>]  
> [-maxDepth <max_depth_of_weak_tree = 1>]  
> [-maxWeakCount <max_weak_tree_count = 100>]  
>--haarFeatureParams--  
> [-mode <BASIC(default) | CORE | ALL  
>--lbpFeatureParams--  
>--HOGFeatureParams--  

###Example:
`opencv_traincascade -data doors -vec doors.vec -bg background.idx -numPos 255 -numNeg 773 -numStages 15 -numThreads 4 -stageType BOOST -w 100 -h 230 -featureType LBP -minHitRate 0.999995 -maxFalseAlarmRate 0.42 -maxDepth 10 -maxWeakCount 120 -mode ALL`


####Using

`opencv_traincascade -data doors -vec doors.vec -bg background.idx -numPos 774 -numNeg 1004 -numStages 2 -featureType LBP -numThreads 4 -stageType BOOST -w 100 -h 230 -minHitRate 0.999995 -maxFalseAlarmRate 0.42 -maxWeakCount 120 -mode ALL -maxdepth 4`

`opencv_traincascade -data doors -vec doors.vec -bg background.idx -numPos 50 -numNeg 100 -numStages 2 -featureType LBP -numThreads 4 -stageType BOOST -w 100 -h 230 -minHitRate 0.999995 -maxFalseAlarmRate 0.42 -maxWeakCount 120 -mode ALL-maxdepth 4`

`opencv_traincascade -data doors -vec doors.vec -bg background.idx -numPos 50 -numNeg 50 -numStages 2 -featureType LBP -numThreads 4 -stageType BOOST -w 100 -h 230 -minHitRate 0.999995 -maxFalseAlarmRate 0.42 -maxWeakCount 120 -mode ALL`

`opencv_traincascade -data doors -vec doors.vec -bg background.idx -numPos 50 -numNeg 50 -numStages 2 -featureType LBP -numThreads 4 -stageType BOOST -w 100 -h 230 -minHitRate 0.999995 -maxFalseAlarmRate 0.42 -maxWeakCount 120 -mode ALL`