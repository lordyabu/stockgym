import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Masking
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Example data (list of sequences with variable lengths)
sequences = [
    [1, 2, 3],
    [1, 2, 3, 4, 5, 6],
    [1, 2]
]

# Pad sequences for equal length
max_sequence_length = max(len(sequence) for sequence in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')

# Build the LSTM model
model = Sequential()
model.add(Masking(mask_value=0., input_shape=(max_sequence_length, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(1, activation='linear'))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Summary of the model
model.summary()

# Assuming you have your targets stored in `targets`
# targets = [...]

# Fit the model (example, replace `targets` with your actual targets)
# model.fit(padded_sequences, targets, epochs=10, batch_size=32)
