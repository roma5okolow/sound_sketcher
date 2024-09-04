import numpy as np
from scipy.fft import fft, ifft

PI = np.pi


def create_frames(data: np.ndarray, hop: int, win_size: int) -> np.ndarray:
    '''
    Creates overlapping windows for the stft implementation.

    Args:
        data: array_like
            Input signal for window splitting.
        hop: int
            Number of samples between successive windows on analysis stage.
        win_size: int
            Number of samples in window.

    Returns:
        vector_frames: array_like
            Matrix of successive windows with shape (num_slices, win_size).
    '''

    num_slices = (len(data) - win_size) // hop + 1
    data = data[:num_slices * hop + win_size]
    vector_frames = np.zeros((num_slices, win_size))

    for index in range(num_slices):
        indexTimeStart = index*hop
        indexTimeEnd = index*hop + win_size
        vector_frames[index, :] = data[indexTimeStart:indexTimeEnd]

    return vector_frames


def fusion_frames(frames_matrix: np.ndarray, hop: int) -> np.ndarray:
    '''
    Performs overlap-add of the synthesis frames.

    Args:
        frames_matrix: array_like
            Matrix of successive windows.
        hop: int
            Number of samples between successive windows on synthesis stage.

    Returns:
        vector_time: array_like
            Output signal.
    '''

    number_frames, size_frames = frames_matrix.shape
    vector_time = np.zeros(number_frames*hop-hop+size_frames)

    time_ind = 0
    for index in range(number_frames):
        vector_time[time_ind:time_ind+size_frames] += frames_matrix[index]
        time_ind += hop

    return vector_time


def signal_stretcher(x: np.ndarray, ratio: int, win_size: int = 1024, an_hop=256) -> np.ndarray:

    '''
    Performs signal stretching without changing the tone.
    PhaseVocoder algorithm is used to adjust the phase in frequency domain.

    Args:
        x: array_like
            Input signal.
        ratio: real positive
            The signal will be stretched by about time_stretch_ratio times.
        win_size: int
            Number of samples in window.
        an_hop: int
            Number of samples between successive windows on analysis stage.

    Returns:
        output_stretched: array_like
            Output signal streched by ratio times.
    '''

    syn_hop = round(ratio*an_hop)

    wn = np.hanning(win_size)

    # Zero-padding
    x = np.pad(x, (an_hop * 3, 0))

    # Initialization
    input_frames = create_frames(x, an_hop, win_size)
    num_frames = input_frames.shape[0]
    output = np.zeros((num_frames, win_size))
    win_grid = np.arange(win_size)
    phase_cumulative = 0
    previous_phase = 0

    for ind in range(num_frames):
        # Analysis
        cur_frame = input_frames[ind]
        cur_frame_wind = cur_frame * wn / np.sqrt(((win_size/an_hop)/2))
        cur_frame_wind_fft = fft(cur_frame_wind)
        magn_frame = np.abs(cur_frame_wind_fft)
        phase_frame = np.angle(cur_frame_wind_fft)

        # Processing
        delta_phi = phase_frame - previous_phase
        previous_phase = phase_frame
        delta_phi -= an_hop * 2 * PI * win_grid / win_size
        delta_phi = (delta_phi + PI) % (2 * PI) - PI
        true_freq = 2 * PI * win_grid / win_size + delta_phi / an_hop
        phase_cumulative = phase_cumulative + syn_hop * true_freq

        # Synthesis
        output_frame = ifft(magn_frame * np.exp(1j * phase_cumulative)).real
        output[ind] = output_frame * wn / np.sqrt(((win_size / syn_hop) / 2))

    # Fusion
    output_stretched = fusion_frames(output, syn_hop)

    return output_stretched