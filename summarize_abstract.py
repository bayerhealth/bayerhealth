def summarize_title(text):
    from eazymind.nlp.eazysum import Summarizer
    key = "b47b7ffea86caab6112d2cf190b0b5d6"
    sentence = str(text.encode('utf-8'))
    summarizer = Summarizer(key)
    i="i"
    while(1):
        i=summarizer.run(sentence)
        wyn=i.split()
        print(wyn)
        if(wyn[0][0]!="<"):
            x=""
            for y in wyn[1:7]:
                if len(y)>=2:
                    x=x+" "+y
            return x
