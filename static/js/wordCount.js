/**
 * Word count tracking for submission forms
 * Tracks word count and provides visual feedback
 */

document.addEventListener('DOMContentLoaded', function() {
    const answerTextarea = document.getElementById('answer_text');
    const wordCountDisplay = document.getElementById('word_count');
    const wordLimitDisplay = document.getElementById('word_limit');
    const wordProgress = document.getElementById('word_progress');
    const submissionForm = document.getElementById('submission_form');
    
    if (answerTextarea && wordCountDisplay) {
        // Get the word limit from the display
        const wordLimit = wordLimitDisplay ? parseInt(wordLimitDisplay.textContent) : 500;
        
        // Initial word count
        updateWordCount();
        
        // Update word count when text changes
        answerTextarea.addEventListener('input', updateWordCount);
        
        // Function to count words and update display
        function updateWordCount() {
            // Count words (split by whitespace and filter out empty strings)
            const text = answerTextarea.value.trim();
            const wordCount = text ? text.split(/\s+/).filter(word => word.length > 0).length : 0;
            
            // Update display
            wordCountDisplay.textContent = wordCount;
            
            // Update progress bar if it exists
            if (wordProgress) {
                const percentage = Math.min((wordCount / wordLimit) * 100, 100);
                wordProgress.style.width = percentage + '%';
                
                // Change color based on word count
                if (wordCount < wordLimit * 0.5) {
                    wordProgress.className = 'progress-bar bg-danger';
                } else if (wordCount < wordLimit * 0.9) {
                    wordProgress.className = 'progress-bar bg-warning';
                } else if (wordCount <= wordLimit) {
                    wordProgress.className = 'progress-bar bg-success';
                } else {
                    wordProgress.className = 'progress-bar bg-danger';
                }
            }
            
            // Add or remove warning class
            if (wordCount > wordLimit) {
                wordCountDisplay.classList.add('text-danger');
                wordCountDisplay.classList.add('fw-bold');
            } else {
                wordCountDisplay.classList.remove('text-danger');
                wordCountDisplay.classList.remove('fw-bold');
            }
        }
        
        // Add form validation for word count
        if (submissionForm) {
            submissionForm.addEventListener('submit', function(event) {
                const wordCount = answerTextarea.value.trim().split(/\s+/).filter(word => word.length > 0).length;
                
                if (wordCount < wordLimit * 0.5) {
                    event.preventDefault();
                    alert('Your answer is too short. Please write at least ' + Math.ceil(wordLimit * 0.5) + ' words.');
                }
            });
        }
        
        // Add animation to the word count display
        answerTextarea.addEventListener('input', function() {
            wordCountDisplay.classList.add('animate__animated', 'animate__pulse');
            setTimeout(function() {
                wordCountDisplay.classList.remove('animate__animated', 'animate__pulse');
            }, 500);
        });
    }
});
