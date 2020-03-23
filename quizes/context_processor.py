def total_correct_answer(request):
    correct = 0
    if request.user.is_authenticated:
        if not request.user.is_staff:
            try:

                if request.session['answer']:
                    for key, value in request.session['answer'].items():
                        if value['points'] == 1:
                            correct += 1
            except Exception as e:
                pass
        return {'total_correct_answer': correct}
    else:
        return {'total_correct_answer': 0}
