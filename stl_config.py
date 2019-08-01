class Config():

    def __init__(self, base_directory_path):

        self.base_directory_path = base_directory_path + "/"
        self.base_directory_model = self.base_directory_path + "model/"
        self.base_directory_data = base_directory_path + "data/"
        self.file_conll_train_data = self.base_directory_data + "train.data"
        self.file_seq_train_data = self.file_conll_train_data + ".seq"

        self.file_full_word_embedding = self.base_directory_path + "we.vec"
        self.file_trimmed_word_embedding = self.base_directory_model + "word_embedding.trimmed"
        self.file_word_vocab = self.base_directory_model + "vocab.words"
        self.file_char_vocab = self.base_directory_model + "vocab.chars"
        self.file_tag_vocab = self.base_directory_model + "vocab.tags"

        self.dir_tensoboard_log = "log/"
        self.dir_checkpoints = self.base_directory_model

        self.word_embedding_dimension        = 300
        self.char_embedding_dimension        = 100

        #LSTM_MODE
        self.lstm_model_batch_size           = 32
        self.lstm_model_hidden_size          = 300
        self.lstm_model_rnn_dropout          = 0.5
        self.lstm_model_rnn_lr               = 0.001
        self.lstm_model_max_epoch            = 40
        self.lstm_model_hidden_size_char     = 100


        #Model
        self.max_char                        = 65