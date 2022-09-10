#!/usr/bin/env python
# encoding: utf-8
"""
summarization.py
"""

from transformers import MBartForConditionalGeneration, AutoTokenizer

def summarize(text, tokenizer, model):
    input_ids = tokenizer(
        [text],
        max_length=600,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        top_k=0,
        num_beams=3,
        no_repeat_ngram_size=3
    )[0]


    result = tokenizer.decode(output_ids, skip_special_tokens=True)
    return result[:500] if len(result) > 500 else result


def getSummarizer():
    model_name = "Kirili4ik/mbart_ruDialogSum"   
    tokenizer =  AutoTokenizer.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    model.eval()

    return lambda text: summarize(text, tokenizer, model)