class AndaluhToCasTranscriptor:
    class __AndaluhToCasTranscriptor:
        def __init__(self):
            import pickle
            import pathlib
            from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM

            root_path = pathlib.Path(__file__).parent.parent
            dict_path = root_path / "data/inv_dict.pickle"
            with open(dict_path, 'rb') as handle:
                self.inv_dict = pickle.load(handle)

                # BERTO tokenizer and MaskedLM model
            models_path = root_path / "models/bert-base-spanish-wwm-cased"
            self.tokenizer = BertTokenizer.from_pretrained(models_path, do_lower_case=False)
            self.bertMaskedLM = BertForMaskedLM.from_pretrained(models_path)

    __instance = None
    __nlp = None

    def __init__(self):
        if not AndaluhToCasTranscriptor.__instance:
            import spacy
            AndaluhToCasTranscriptor.__instance = AndaluhToCasTranscriptor.__AndaluhToCasTranscriptor()
            AndaluhToCasTranscriptor.__nlp = spacy.load('es_core_news_sm')

    def getTransliteration(self, token):
        return self.__instance.inv_dict[token]

    def transcript(self, text):
        transcription = []
        options = []
        doc = self.__nlp(text)
        for token in doc:
            if token.pos_ in ('PUNCT', 'NUM', 'SYM'):
                transcription.append(token.text)
            else:
                if token.text.lower() in self.__instance.inv_dict:
                    transliteral = self.getTransliteration(token.text.lower())
                    if len(transliteral) > 1:
                        next_token = transliteral
                    else:
                        next_token = next(iter(transliteral))
                else:
                    next_token = '{NOT_FOUND}'
                transcription.append(next_token)
            if token.whitespace_:
                transcription.append(" ")

        candidates = self.__generate_candidates(transcription)
        ranked_candidates =  self.__rank_candidates(candidates)
        return ranked_candidates

    # TODO these helpers can be static. Move them to a utils o helpers file
    def __generate_candidates(self, transcriptions):
        import itertools
        candidates = []
        options = [x for x in transcriptions if isinstance(x, set)]
        combinations = itertools.product(*options)
        for tuple in combinations:
            index = 0
            next_candidate = []
            for element in transcriptions:
                if isinstance(element, set):
                    next_candidate.append(tuple[index])
                    index += 1
                else:
                    next_candidate.append(element)
            candidates.append("".join(next_candidate))
        return candidates

    def __rank_candidates(self, candidates):
        scored_candidates = []
        for candidate in candidates:
            scored_candidates.append((self.__get_candidate_score(candidate), candidate))
        return sorted(scored_candidates, key=lambda x: x[0])


    def __get_candidate_score(self, sentence):
        import torch, math
        tokenize_input = self.__instance.tokenizer.tokenize(sentence)
        tensor_input = torch.tensor([self.__instance.tokenizer.convert_tokens_to_ids(tokenize_input)])
        predictions = self.__instance.bertMaskedLM(tensor_input)
        loss_fct = torch.nn.CrossEntropyLoss()
        loss = loss_fct(predictions.squeeze(), tensor_input.squeeze()).data
        return math.exp(loss)


