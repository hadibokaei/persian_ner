import tensorflow as tf
from common.utility import setup_custom_logger
from model.base_model import Model
import os

class MTL4CharCNNWordBilstmModel(Model):

    def __init__(self, vocab_size, dim, task1_tag_size, task2_tag_size, task3_tag_size, task4_tag_size, max_word_len, char_emb_dim, lstm_size, learning_rate
                 , tensorboard_log, chkpnts_path, char_size):
        self.vocab_size = vocab_size
        self.dim = dim
        self.task1_tag_size = task1_tag_size
        self.task2_tag_size = task2_tag_size
        self.task3_tag_size = task3_tag_size
        self.task4_tag_size = task4_tag_size
        self.char_size = char_size
        self.logger = setup_custom_logger(__name__)
        self.max_word_len = max_word_len
        self.char_emb_dim = char_emb_dim
        self.lstm_size = lstm_size
        self.learning_rate = learning_rate
        self.tensorboard_log = tensorboard_log
        self.chkpnts_path = chkpnts_path
        print('MTL2CharCNNWordBilstmModel')

        return

    def add_lstm(self):
        with tf.variable_scope('task1_bilstm'):
            cell_fw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            cell_bw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=cell_fw,
                cell_bw=cell_bw,
                inputs=self.embedded_words,
                sequence_length=self.sentence_lenghts,
                dtype=tf.float32)
            task1_output_word = tf.concat([outputs_fw, outputs_bw], axis=2)

        with tf.variable_scope('task2_bilstm'):
            cell_fw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            cell_bw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=cell_fw,
                cell_bw=cell_bw,
                inputs=self.embedded_words,
                sequence_length=self.sentence_lenghts,
                dtype=tf.float32)
            task2_output_word = tf.concat([outputs_fw, outputs_bw], axis=2)

        with tf.variable_scope('task3_bilstm'):
            cell_fw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            cell_bw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=cell_fw,
                cell_bw=cell_bw,
                inputs=self.embedded_words,
                sequence_length=self.sentence_lenghts,
                dtype=tf.float32)
            task3_output_word = tf.concat([outputs_fw, outputs_bw], axis=2)

        with tf.variable_scope('task4_bilstm'):
            cell_fw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            cell_bw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=cell_fw,
                cell_bw=cell_bw,
                inputs=self.embedded_words,
                sequence_length=self.sentence_lenghts,
                dtype=tf.float32)
            task4_output_word = tf.concat([outputs_fw, outputs_bw], axis=2)

        with tf.variable_scope('shared_bilstm'):
            cell_fw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            cell_bw = tf.contrib.rnn.LSTMCell(num_units=self.lstm_size)
            (outputs_fw, outputs_bw), _ = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=cell_fw,
                cell_bw=cell_bw,
                inputs=self.embedded_words,
                sequence_length=self.sentence_lenghts,
                dtype=tf.float32)
            shared_output_word = tf.concat([outputs_fw, outputs_bw], axis=2)

        task1_lstm_layer_output = tf.concat([task1_output_word, shared_output_word], axis = 2)
        self.task1_lstm_layer_output = tf.nn.dropout(task1_lstm_layer_output, self.dropout)

        task2_lstm_layer_output = tf.concat([task2_output_word, shared_output_word], axis = 2)
        self.task2_lstm_layer_output = tf.nn.dropout(task2_lstm_layer_output, self.dropout)

        task3_lstm_layer_output = tf.concat([task3_output_word, shared_output_word], axis=2)
        self.task3_lstm_layer_output = tf.nn.dropout(task3_lstm_layer_output, self.dropout)

        task4_lstm_layer_output = tf.concat([task4_output_word, shared_output_word], axis=2)
        self.task4_lstm_layer_output = tf.nn.dropout(task4_lstm_layer_output, self.dropout)

    def add_fcn(self):
        with tf.variable_scope('task1_fcn'):
            task1_W = tf.get_variable(name="task1_W", dtype=tf.float32, shape=[4 * self.lstm_size, self.task1_tag_size])
            task1_b = tf.get_variable(name="task1_b", dtype=tf.float32, shape=[self.task1_tag_size], initializer=tf.zeros_initializer())
            nsteps = tf.shape(self.task1_lstm_layer_output)[1]
            output = tf.reshape(self.task1_lstm_layer_output, shape=[-1, 4 * self.lstm_size])
            output = tf.matmul(output, task1_W) + task1_b
            self.task1_logits = tf.reshape(output, shape=[-1, nsteps, self.task1_tag_size])

        with tf.variable_scope('task2_fcn'):
            task2_W = tf.get_variable(name="task2_W", dtype=tf.float32, shape=[4 * self.lstm_size, self.task2_tag_size])
            task2_b = tf.get_variable(name="task2_b", dtype=tf.float32, shape=[self.task2_tag_size], initializer=tf.zeros_initializer())
            nsteps = tf.shape(self.task2_lstm_layer_output)[1]
            output = tf.reshape(self.task2_lstm_layer_output, shape=[-1, 4 * self.lstm_size])
            output = tf.matmul(output, task2_W) + task2_b
            self.task2_logits = tf.reshape(output, shape=[-1, nsteps, self.task2_tag_size])

        with tf.variable_scope('task3_fcn'):
            task3_W = tf.get_variable(name="task3_W", dtype=tf.float32,
                                      shape=[4 * self.lstm_size, self.task3_tag_size])
            task3_b = tf.get_variable(name="task3_b", dtype=tf.float32, shape=[self.task3_tag_size],
                                      initializer=tf.zeros_initializer())
            nsteps = tf.shape(self.task3_lstm_layer_output)[1]
            output = tf.reshape(self.task3_lstm_layer_output, shape=[-1, 4 * self.lstm_size])
            output = tf.matmul(output, task3_W) + task3_b
            self.task3_logits = tf.reshape(output, shape=[-1, nsteps, self.task3_tag_size])

        with tf.variable_scope('task4_fcn'):
            task4_W = tf.get_variable(name="task4_W", dtype=tf.float32,
                                      shape=[4 * self.lstm_size, self.task4_tag_size])
            task4_b = tf.get_variable(name="task4_b", dtype=tf.float32, shape=[self.task4_tag_size],
                                      initializer=tf.zeros_initializer())
            nsteps = tf.shape(self.task4_lstm_layer_output)[1]
            output = tf.reshape(self.task4_lstm_layer_output, shape=[-1, 4 * self.lstm_size])
            output = tf.matmul(output, task4_W) + task4_b
            self.task4_logits = tf.reshape(output, shape=[-1, nsteps, self.task4_tag_size])

    def add_train_op(self):

        with tf.variable_scope('task1_loss'):
            log_likelihood, self.task1_transition_param = tf.contrib.crf.crf_log_likelihood(self.task1_logits, self.labels, self.sentence_lenghts)
            self.loss = tf.reduce_mean(-log_likelihood)
            self.task1_train = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
            self.task1_trainloss = tf.summary.scalar('task1 train batch loss', self.loss)
            self.task1_validationloss = tf.summary.scalar('task1 validation loss', self.loss)

        with tf.variable_scope('task2_loss'):
            log_likelihood, self.task2_transition_param = tf.contrib.crf.crf_log_likelihood(self.task2_logits, self.labels, self.sentence_lenghts)
            self.task2_loss = tf.reduce_mean(-log_likelihood)
            self.task2_train = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.task2_loss)
            self.task2_trainloss = tf.summary.scalar('task2 train batch loss', self.task2_loss)
            self.task2_validationloss = tf.summary.scalar('task2 validation loss', self.task2_loss)

        with tf.variable_scope('task3_loss'):
            log_likelihood, self.task3_transition_param = tf.contrib.crf.crf_log_likelihood(self.task3_logits, self.labels, self.sentence_lenghts)
            self.task3_loss = tf.reduce_mean(-log_likelihood)
            self.task3_train = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.task3_loss)
            self.task3_trainloss = tf.summary.scalar('task3 train batch loss', self.task3_loss)
            self.task3_validationloss = tf.summary.scalar('task3 validation loss', self.task3_loss)

        with tf.variable_scope('task4_loss'):
            log_likelihood, self.task4_transition_param = tf.contrib.crf.crf_log_likelihood(self.task4_logits, self.labels, self.sentence_lenghts)
            self.task4_loss = tf.reduce_mean(-log_likelihood)
            self.task4_train = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.task4_loss)
            self.task4_trainloss = tf.summary.scalar('task4 train batch loss', self.task4_loss)
            self.task4_validationloss = tf.summary.scalar('task4 validation loss', self.task4_loss)

    def train_graph(self, main_task_train_word_seq, main_task_train_tag_seq, main_task_train_char_seq,
                    aux_task1_train_word_seq, aux_task1_train_tag_seq, aux_task1_train_char_seq,
                    aux_task2_train_word_seq, aux_task2_train_tag_seq, aux_task2_train_char_seq,
                    aux_task3_train_word_seq, aux_task3_train_tag_seq, aux_task3_train_char_seq,
                    val_word_seq, val_tag_seq, val_char_seq,
                    word_embedding, epoch_start, epoch_end, batch_size):

        task1_num_sen = len(main_task_train_word_seq)
        task2_num_sen = len(aux_task1_train_word_seq)
        task3_num_sen = len(aux_task2_train_word_seq)
        task4_num_sen = len(aux_task3_train_word_seq)

        total_counter = 0
        batch_number_task1 = 0
        batch_number_task2 = 0
        batch_number_task3 = 0
        batch_number_task4 = 0
        end_index_task1 = 0
        end_index_task2 = 0
        end_index_task3 = 0
        end_index_task4 = 0

        best_val_acc = 0
        for epoch in range(epoch_start, epoch_end):
            batch_number_task1 = 0
            end_index_task1 = 0
            while end_index_task1 < task1_num_sen:
                total_counter += 1

                if end_index_task2 == task2_num_sen:
                    end_index_task2 = 0
                    batch_number_task2 = 0

                if end_index_task3 == task3_num_sen:
                    end_index_task3 = 0
                    batch_number_task3 = 0

                if end_index_task4 == task4_num_sen:
                    end_index_task4 = 0
                    batch_number_task4 = 0


                start_index_task1 = batch_number_task1 * batch_size
                end_index_task1 = min([start_index_task1 + batch_size, task1_num_sen])

                start_index_task2 = batch_number_task2 * batch_size
                end_index_task2 = min([start_index_task2 + batch_size, task2_num_sen])

                start_index_task3 = batch_number_task3 * batch_size
                end_index_task3 = min([start_index_task3 + batch_size, task3_num_sen])

                start_index_task4 = batch_number_task4 * batch_size
                end_index_task4 = min([start_index_task4 + batch_size, task4_num_sen])

                feed_dict, current_batch_len, current_batch_word_seq, current_batch_tag_seq = \
                    self.create_feed_dict(main_task_train_word_seq, main_task_train_tag_seq, main_task_train_char_seq, word_embedding, start_index_task1, end_index_task1, 0.5)
                [summary, _, loss] = self.sess.run([self.task1_trainloss, self.task1_train, self.loss], feed_dict)
                if batch_number_task1 % 50 == 0:
                    self.writer.add_summary(summary, total_counter)
                    self.logger.info("epoch: {} batch: {} task: 1 loss on train: {}".format(epoch, batch_number_task1, loss))

                feed_dict, current_batch_len, current_batch_word_seq, current_batch_tag_seq = \
                    self.create_feed_dict(aux_task1_train_word_seq, aux_task1_train_tag_seq, aux_task1_train_char_seq, word_embedding, start_index_task2, end_index_task2, 0.5)
                [summary, _, loss] = self.sess.run([self.task2_trainloss, self.task2_train, self.task2_loss], feed_dict)
                if batch_number_task2 % 50 == 0:
                    self.writer.add_summary(summary, total_counter)
                    self.logger.info("epoch: {} batch: {} task: 2 loss on train: {}".format(epoch, batch_number_task2, loss))

                feed_dict, current_batch_len, current_batch_word_seq, current_batch_tag_seq = \
                    self.create_feed_dict(aux_task2_train_word_seq, aux_task2_train_tag_seq, aux_task2_train_char_seq, word_embedding, start_index_task3, end_index_task3, 0.5)
                [summary, _, loss] = self.sess.run([self.task3_trainloss, self.task3_train, self.task3_loss], feed_dict)
                if batch_number_task3 % 50 == 0:
                    self.writer.add_summary(summary, total_counter)
                    self.logger.info("epoch: {} batch: {} task: 3 loss on train: {}".format(epoch, batch_number_task3, loss))

                feed_dict, current_batch_len, current_batch_word_seq, current_batch_tag_seq = \
                    self.create_feed_dict(aux_task3_train_word_seq, aux_task3_train_tag_seq, aux_task3_train_char_seq, word_embedding, start_index_task4, end_index_task4, 0.5)
                [summary, _, loss] = self.sess.run([self.task4_trainloss, self.task4_train, self.task4_loss], feed_dict)
                if batch_number_task4 % 50 == 0:
                    self.writer.add_summary(summary, total_counter)
                    self.logger.info("epoch: {} batch: {} task: 4 loss on train: {}".format(epoch, batch_number_task4, loss))

                batch_number_task1 += 1
                batch_number_task2 += 1
                batch_number_task3 += 1
                batch_number_task4 += 1

            # choice1: save model after each epoch and terminate after specified epoch number
            save_path = self.saver.save(self.sess, os.path.join(self.chkpnts_path, "mtl4_ner"),
                                        global_step=int(epoch), write_meta_graph=False)
            self.logger.info("model is saved in: {}{}".format(save_path, ''.join([' '] * 100)))

            self.writer.add_summary(summary, epoch)
            acc = self.evaluate_model(val_word_seq, val_tag_seq, val_char_seq, word_embedding, batch_size)

            if acc > best_val_acc:
                tf.saved_model.save(self, os.path.join(self.chkpnts_path, "final"))
                best_val_acc = acc

            self.logger.info("epoch: {} accuracy on validation: {}".format(epoch, acc))

