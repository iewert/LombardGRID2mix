import sys
from os import path
import os
import librosa
import random
import soundfile as sf


# set path to pyAcoustics package, WSJ dataset and root path
pyacoustics_path = 'path/to/pyAcoustics/'
wsj_path = '/path/to/wsj/wsj_raw_single_speaker_8k/'
root_path = '/path/to/LombardGRID2mix_Scripts/'
noise_levels = [3, -2.5, -8.0, -13.5]
subsets = ['tr', 'cv', 'tt']

sys.path.append(path.abspath(pyacoustics_path))
from pyacoustics.speech_filters.speech_shaped_noise import generateNoise


def create_folder(path):
    """
    Create a folder if not existent at the specified path.
 
    Args:
        path (str): The path where the folder should be generated.
    """
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def create_noise_folder_structure():
    """
    Creates the output folder structure for the noise files and samples.
 
    Returns:
        output_paths (Dict): The output paths for the noise files.

    """

    output_path_noise_files = root_path + '/data_and_mixing_instructions/Lombardgrid/Noise_Files/'
    create_folder(output_path_noise_files)
    output_paths = {'train' : output_path_noise_files + 'noise_train_val_speakers/',
                'test' : output_path_noise_files + 'noise_test_speakers/'}
    for path in output_paths.values():
        create_folder(path)
    create_folder(output_path_noise_files + 'noise_samples')
    
    return output_paths


def generate_noise_files_per_set():
    """
    Generates noise files for the test and train/validation case separately..
 
    Returns:
        output_paths (Dict): The output paths for the noise files.

    """

    output_paths = create_noise_folder_structure()
    evaluation_dir = wsj_path + 'si_et_05_8k'
    development_dir = wsj_path + 'si_dt_05_8k'
    train_dir = wsj_path + 'si_tr_s_8k_all'
    train_spk_dirs = [os.path.join(train_dir, t) for t in os.listdir(train_dir)]
    test_spk_dirs = [os.path.join(evaluation_dir, t) for t in os.listdir(evaluation_dir)] + [os.path.join(development_dir, t) for t in os.listdir(development_dir)]

    input_paths = {'train': train_spk_dirs,
               'test': test_spk_dirs}
    
    for name, dir_set in input_paths.items():
        generate_noise_files(dir_set, output_paths[name])

    return output_paths

def generate_noise_files(dir_set, output_path):
    """
    Generates for each WSJ0 speaker a speech-shaped noise file.
    
    Args:
        dir_set (list): List of the WSJ0 speaker folders.
        output_path (str): Output path for the noise files.
    
    """
    spk_file_dict = {}
    for dir in dir_set:
        for _,_,files in os.walk(dir):
            for file in files:
                spk_id = os.path.basename(dir)
                if spk_id in spk_file_dict.keys():
                    spk_file_dict[spk_id].append(os.path.join(dir, file))
                else:
                    spk_file_dict[spk_id] = [os.path.join(dir, file)]

    for spk_id in spk_file_dict.keys():
                output_file = output_path + 'ssn_noise_' + str(spk_id) + '.wav'
                generateNoise(spk_file_dict[spk_id], output_file)

def create_mixture_instruction(noise_level, subset, input_paths):
    """
    Creates a two speaker plus noise list for the simulation process and the specified subset. 
    
    Args:
        noise_level (float): Deterministic noise level in dB.
        subset (str): Abbreviated name of the subset.
        input_paths (Dict): The input paths for the noise files.

    Returns:
        output_file (str): Path of the generated mixture instruction file. 
    
    """

    path_noise_samples = 'data_and_mixing_instructions/Lombardgrid/Noise_Files/noise_samples/' + subset + '/'
    output_path_noise_samples = root_path + path_noise_samples
    create_folder(output_path_noise_samples)
    output_file = root_path + 'data_and_mixing_instructions/' + 'mix_l_'+ subset + '_noisy_' + str(noise_level) + '.txt'
    
    if subset == 'tt':
        noise_file_path = input_paths['test']
    else: 
        noise_file_path = input_paths['train']

    instruction_file_wo_noise = open(root_path + '/data_and_mixing_instructions/'+ 'mix_l_'+ subset + '.txt' , 'r')
    mixture_instructions = instruction_file_wo_noise.readlines()
    mix_files_1_audio = [librosa.load(os.path.join(os.path.join(root_path, '/data_and_mixing_instructions/'), f.split()[0])) for f in mixture_instructions]
    mix_files_2_audio = [librosa.load(os.path.join(os.path.join(root_path, '/data_and_mixing_instructions/'), f.split()[2])) for f in mixture_instructions]
    noise_file_names = os.listdir(noise_file_path)
    noise_audios = {f: librosa.load(os.path.join(noise_file_path, f)) for f in noise_file_names}
    noise_files_time_stamps = { noise_filename : 0 for noise_filename in noise_file_names }

    for i, instruction in enumerate(mixture_instructions):
    # sample uniformly ssn noise file from list
        min_len = min(len(mix_files_1_audio[i][0]), len(mix_files_2_audio[i][0]))
        noise_filename = random.choice(noise_file_names)
        noise_file, sr = noise_audios[noise_filename]
        while (noise_files_time_stamps[noise_filename] + min_len) > len(noise_file):
            noise_file_names.remove(noise_filename)
            # reset if all noise samples are used
            if len(noise_file_names) == 0:
                noise_file_names = os.listdir(noise_file_path)
                noise_files_time_stamps = { noise_filename : 0 for noise_filename in noise_file_names }
            noise_filename = random.choice(noise_file_names)
        noise_file_samp = noise_file[noise_files_time_stamps[noise_filename]:(noise_files_time_stamps[noise_filename]+min_len)]
        noise_samp_name = noise_filename.split('.')[0] + '_' + str(noise_files_time_stamps[noise_filename]) + '_' + str((noise_files_time_stamps[noise_filename]+min_len)) + '.wav'
        noise_files_time_stamps[noise_filename] = noise_files_time_stamps[noise_filename]+ min_len
        sf.write((output_path_noise_samples + noise_samp_name), noise_file_samp, sr)
        path_noise_file_short = '/'.join(path_noise_samples.split('/')[1:])+ '/' + subset + '/' + noise_samp_name
        mix_instr_wo = mixture_instructions[i].replace('\n', '')
        mixture_instructions[i] = mix_instr_wo + ' ' + path_noise_file_short + ' ' + str(noise_level)
        with open((output_file), 'a') as f:
            f.write(mixture_instructions[i] + '\n')

    return output_file


def duplicate_instruction_files_for_noise_levels(instruction_file, noise_levels, subset):
    """
    Duplicates a two speaker plus noise list for the other specified noise levels and adapts the nosie level. 
    
    Args:
        instruction_file (str): Path to the mixture instruction file that needs to be duplicated.
        noise_levels (list): List of noise levels.
        subset (str): Abbreviated subset name.

    Returns:
        output_file (str): Path of the generated mixture instruction file. 
    
    """
    template = open(instruction_file, 'r')
    template_instructions = template.readlines()

    for level in noise_levels:
        output_file = root_path + 'data_and_mixing_instructions/' + 'mix_l_'+ subset + '_noisy_'+ str(level) + '.txt'
        for m in template_instructions:
            m = m.split()[:-1]
            m = ' '.join(m)
            with open(output_file, 'a') as f:
                f.write(m + ' ' + str(level) + '\n')
     


def main():
    # generate noise files for test set and training/validation set on the basis of the WSJ0 speaker's audio material
    output_paths = generate_noise_files_per_set()
    # for each Lombard subset (training, validation, testing) create four mixing instruction files 
    # (each with a different noise level)
    for subset in subsets:     
        instruction_file = create_mixture_instruction(noise_levels[0], subset, output_paths)
        duplicate_instruction_files_for_noise_levels(instruction_file, noise_levels[1:], subset)
     

if __name__ == "__main__":
    main()
     



