"""polls 應用程式的視圖函式。"""

from django.shortcuts import render, get_object_or_404, redirect

from .models import Question, Choice, Vote


def index(request):
    question_list = Question.objects.order_by("-pub_date")
    print(question_list)
    context = {"question_list": question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    """
    處理對特定問題的投票行為。

    參數:
        request: HttpRequest 物件
        question_id: 問題的主鍵

    回傳:
        HttpResponse 物件
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method != "POST":
        return redirect("polls:detail", question_id=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    user = request.user
    existing_vote = Vote.objects.filter(user=user, question=question).first()
    if existing_vote:
        if existing_vote.choice != selected_choice:
            old_choice = existing_vote.choice
            old_choice.votes = max(old_choice.votes - 1, 0)
            old_choice.save()
            selected_choice.votes += 1
            selected_choice.save()
            existing_vote.choice = selected_choice
            existing_vote.save()
    else:
        Vote.objects.create(user=user, question=question, choice=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()

    return redirect("polls:results", question_id=question_id)
