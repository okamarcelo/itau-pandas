def carregarTimeline(dataAtual):
    timeline = []
    for evento in eventos:
        if evento.data == dataAtual:
            timeline.append(evento)
    return timeline