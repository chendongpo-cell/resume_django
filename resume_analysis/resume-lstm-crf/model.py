import torch
import torch.nn as nn

from util import argmax, log_sum_exp

torch.manual_seed(1)


class BiLSTM_CRF(nn.Module):

    def __init__(self, vocab_size, tag_to_ix, embedding_dim, hidden_dim):
        super(BiLSTM_CRF, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)

        self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2,
                            num_layers=1, bidirectional=True)

        # Maps the output of the LSTM into tag space.
        self.hidden2tag = nn.Linear(hidden_dim, self.tagset_size)

        # Matrix of transition parameters.  Entry i,j is the score of
        # transitioning *to* i *from* j.转态转移矩阵
        self.transitions = nn.Parameter(
            torch.randn(self.tagset_size, self.tagset_size))

        # These two statements enforce the constraint that we never transfer
        # to the start tag and we never transfer from the stop tag
        self.transitions.data[tag_to_ix['<start>'], :] = -10000
        self.transitions.data[:, tag_to_ix['<stop>']] = -10000

        # 建立转移矩阵A，并加了两个我们不会变动的约束条件：1、是我们不会从其他tag转向start。
        # 2是不会从stop开始转向其他。所以这些位置设为 - 10000


        self.hidden = self.init_hidden()

    def init_hidden(self):
        return (torch.randn(2, 1, self.hidden_dim // 2),
                torch.randn(2, 1, self.hidden_dim // 2))


    ##依据初始化的参数预测所有路径，返回最大的分数，
    def _forward_alg(self, feats):
        # Do the forward algorithm to compute the partition function
        # .full创建一个1*tagset_size的tensor。内容是-10000,    shape为torch.Size([1, 48])
        init_alphas = torch.full((1, self.tagset_size), -10000.)
        # '<start>' has all of the score.将第一个位置   self.tag_to_ix['<start>']为37
        init_alphas[0][self.tag_to_ix['<start>']] = 0.

        # Wrap in a variable so that we will get automatic backprop    torch.Size([1, 48])
        forward_var = init_alphas

        # Iterate through the sentence,   feat为步长，标签数，这遍历每一步
        for feat in feats:
            emit_score = feat.view(-1, 1)
            tag_var = forward_var + self.transitions + emit_score
            max_tag_var, _ = torch.max(tag_var, dim=1)
            tag_var = tag_var - max_tag_var.view(-1, 1)
            forward_var = max_tag_var + torch.log(torch.sum(torch.exp(tag_var), dim=1)).view(1, -1)

        terminal_var = forward_var + self.transitions[self.tag_to_ix['<stop>']].view(1, -1)
        alpha = log_sum_exp(terminal_var)
        return alpha


    #lstm正向特征提取
    def _get_lstm_features(self, sentence):
        self.hidden = self.init_hidden()
        embeds = self.word_embeds(sentence).view(len(sentence), 1, -1)
        lstm_out, self.hidden = self.lstm(embeds, self.hidden)
        lstm_out = lstm_out.view(len(sentence), self.hidden_dim)
        lstm_feats = self.hidden2tag(lstm_out)
        return lstm_feats

    def _score_sentence(self, feats, tags):
        # Gives the score of a provided tag sequence
        score = torch.zeros(1)
        tags = torch.cat([torch.tensor([self.tag_to_ix['<start>']], dtype=torch.long), tags])
        for i, feat in enumerate(feats):
            score = score + \
                self.transitions[tags[i + 1], tags[i]] + feat[tags[i + 1]]
        score = score + self.transitions[self.tag_to_ix['<stop>'], tags[-1]]
        return score

    def _viterbi_decode(self, feats):

        backpointers = []
        # analogous to forward
        init_vvars = torch.Tensor(1, self.tagset_size).fill_(-10000.)
        init_vvars[0][self.tag_to_ix['<start>']] = 0
        forward_var = init_vvars
        for feat in feats:
            next_tag_var = forward_var.view(1, -1).expand(self.tagset_size, self.tagset_size) + self.transitions
            _, bptrs_t = torch.max(next_tag_var, dim=1)
            bptrs_t = bptrs_t.squeeze().data.cpu().numpy()
            next_tag_var = next_tag_var.data.cpu().numpy()
            viterbivars_t = next_tag_var[range(len(bptrs_t)), bptrs_t]
            viterbivars_t = torch.FloatTensor(viterbivars_t)
            forward_var = viterbivars_t + feat
            backpointers.append(bptrs_t)

        terminal_var = forward_var + self.transitions[self.tag_to_ix['<stop>']]
        terminal_var.data[self.tag_to_ix['<stop>']] = -10000.
        terminal_var.data[self.tag_to_ix['<start>']] = -10000.
        best_tag_id = argmax(terminal_var.unsqueeze(0))
        path_score = terminal_var[best_tag_id]
        best_path = [best_tag_id]
        for bptrs_t in reversed(backpointers):
            best_tag_id = bptrs_t[best_tag_id]
            best_path.append(best_tag_id)
        start = best_path.pop()
        assert start == self.tag_to_ix['<start>']
        best_path.reverse()
        return path_score, best_path

    #正向训练主入口
    def neg_log_likelihood(self, sentence, tags):

        feats = self._get_lstm_features(sentence)
        #前向传播计算score，就是根据lstm的输入加上初始化的状态转移矩阵，计算分数
        forward_score = self._forward_alg(feats)
        #根据真实的tags计算score
        gold_score = self._score_sentence(feats, tags)
        return forward_score - gold_score

    # 预测主入口
    def forward(self, sentence):  # dont confuse this with _forward_alg above.
        # Get the emission scores from the BiLSTM
        lstm_feats = self._get_lstm_features(sentence)

        # Find the best path, given the features.
        score, tag_seq = self._viterbi_decode(lstm_feats)
        return score, tag_seq


