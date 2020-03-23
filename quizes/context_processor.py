def total_correct_answer(request):
    if request.user.is_authenticated:
        correct = 0
        for key, value in request.session['answer'].items():
            if value['points'] == 1:
                correct += 1
        return {'total_correct_answer': correct}
    else:
        return {'total_correct_answer': 0}
