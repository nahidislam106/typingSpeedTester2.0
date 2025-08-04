from django.shortcuts import render
from django.views import View
from .models import TypingTest

class TypingTestView(View):
    def get(self, request):
        # No default text needed now - it will be set via JavaScript
        return render(request, 'typing_test/test.html', {})
    
    def post(self, request):
        text = request.POST.get('text', '')
        typed_text = request.POST.get('typed_text', '')
        time_taken = float(request.POST.get('time_taken', 60))  # in seconds
        
        # Calculate WPM (assuming 5 characters = 1 word)
        word_count = len(typed_text) / 5
        minutes = time_taken / 60
        wpm = round(word_count / minutes, 2) if minutes > 0 else 0
        
        # Calculate accuracy
        correct_chars = sum(1 for a, b in zip(text, typed_text) if a == b)
        accuracy = round((correct_chars / len(text)) * 100, 2) if text else 0
        
        # Save results
        if request.user.is_authenticated:
            TypingTest.objects.create(
                user=request.user,
                text=text,
                wpm=wpm,
                accuracy=accuracy
            )
        
        return render(request, 'typing_test/results.html', {
            'wpm': wpm,
            'accuracy': accuracy,
            'correct_chars': correct_chars,
            'total_chars': len(text),
            'time_taken': round(time_taken, 2)
        })