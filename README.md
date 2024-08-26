# LombardGRID2Mix_Scripts

Here we provide the data split lists and speaker pair lists, and reference the mixing scripts to reproduce the Lombard-GRID-2mix dataset. The dataset is designed to suit the task of blind source separation (BSS) for two speakers and is derived from the Audio-Visual Lombard GRID Speech Corpus [1]. The simulations scripts are based on the ones to create the wsj0-2mix database as used in [2].

## About the data

The Lombard-GRID-2mix dataset consists of two sets: Lombard-GRID-2mix-Normal and Lombard-GRID-2mix-Lombard, containing two-speaker mixtures in normal and Lombard speaking style, respectively. Each set consists of a training, validation and test subset. The simulated subsets contain 109.5, 29, and 9.2 hours (normal) and 118.3, 31.2, and 9.9 hours (Lombard) of total audio data for training, validation, and testing, respectively.
Beyond that, the Lombard set can be simulated with additional background noise (speech-shaped noise) resulting in the Lombard-GRID-2mix-Lombard-noisy set that contains four versions of the Lombard set each characterized by a deterministic noise level. 

## Dataset Simulation
Note that you need Matlab and the Speech Processing Toolbox VOICEBOX ([http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html)) as a prerequisite for the mixing procedures.
Please perform the following steps to recreate the Lombard-GRID-2mix dataset (without additional background noise in the Lombard condition):

1. Download the audio data of all speakers from the Audio-Visual Lombard GRID Speech Corpus ([https://spandh.dcs.shef.ac.uk/avlombard/](https://spandh.dcs.shef.ac.uk/avlombard/)).
2. Split the data into train (tr), validation (cv) and test (tt) once for the normal (Plain) and once for the Lombard (Lombard) condition according to the data lists provided in the corresponding subfolders found in `LombardGRID2mix_Scripts/data_and_mixing_instructions/Lombardgrid/`and save the files in the respective subfolder.
3. Simulate the two-speaker mixtures by utilizing the `create_wav_2speakers.m` Matlab script and the speaker pair lists (see `LombardGRID2mix_Scripts/data_and_mixing_instructions/`). The speaker pair lists are named according to the schema: mix_*condition*_*subset*.txt. Please specify the path to your root and output folders at the top of the script. The mixtures as well as the single sources are saved with a sampling rate of 8 kHz and 16 kHz. 

Please perform the following steps to simulate the Lombard-GRID-2mix-Lombard-noisy subsets (with additional speech-shaped background noise):

1. Get access to the Wall Street Journal corpus (WSJ0) [4] with an appropriate license. This is a prerequisite for the generation of the speech-shaped noise utilized in our experiments. Note that due to the random assignment of noise files to the two-speaker mixtures and by randomly cutting out chunks from these noise files, the background noise can slightly deviate from the noise files utilized in the publication. The strategy, however, is exactly the same as it was pursued in the paper. 
2. Install the requirements in a Conda environment: librosa==0.10.2, numpy==1.22.4, scipy==1.7.3, soundfile==0.12.1. 
3. Clone the pyAcoustics [5] repository ([https://github.com/timmahrt/pyAcoustics/tree/main](https://github.com/timmahrt/pyAcoustics/tree/main)). Replace the file `pyAcoustics/pyacoustics/speech_filters/speech_shaped_noise.py` by the identically named file provided in this repository (see `LombardGRID2mix_Scripts/`).
4. Generate the speaker pair lists (with noise as a pseudo third speaker) by running the script `prepare_speaker_pair_lists_noisy_version.py`. Please specify the path to the WSJ0 dataset, your root path and your path to the pyAcoustics repository at the top of the script beforehand. For each subset of the Lombard condition, four speaker pair lists are generated in the folder `LombardGRID2mix_Scripts/data_and_mixing_instructions/`, each with a different background noise level (3, -2.5, -8.0, -13.5 dB).     
5. Simulate the Lombard-noisy subsets by utilizing the Matlab script `create_wav_3speakers.m`. Please specify the paths to your root folder and your output folders at the top of the script.


## References

[1] N. Alghamdi, S. Maddock, R. Marxer, J. Barker, and G. J. Brown,
“A corpus of audio-visual Lombard speech with frontal and profile
views,” The Journal of the Acoustical Society of America, vol.
143, no. 6, pp. EL523–EL529, 2018.

[2] J. R. Hershey, Z. Chen, J. Le Roux, and S. Watanabe, "Deep Clustering: Discriminative Embeddings for Segmentation and Separation", IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP), DOI: 10.1109/ICASSP.2016.7471631, March 2016, pp. 31-35.

[3] Y. Isik, J. Le Roux, S. Watanabe Z. Chen, and J. R. Hershey, “Scripts to Create wsj0-2 Speaker Mixtures,” MERL Research. Retrieved October
23, 2023, from [https://www.merl.com/demos/deep-clustering/create-speaker-mixtures.zip](https://www.merl.com/demos/deep-clustering/create-speaker-mixtures.zip), [Online].

[4] [https://catalog.ldc.upenn.edu/LDC93S6A](https://catalog.ldc.upenn.edu/LDC93S6A)

[5] Tim Mahrt. PyAcoustics. [https://github.com/timmahrt/pyAcoustics](https://github.com/timmahrt/pyAcoustics), 2016.


## Licenses

- The used mixing scripts to create the Lombard-GRID-2mix dataset are under the Apache 2.0 license, see [3].
- You can get access to the Wall Street Journal corpus (WSJ0) [4] by purchasing an appropriate license.