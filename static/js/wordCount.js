/**
 * Word count functionality for submission forms
 * Tracks word count and provides visual feedback
 */
document.addEventListener('DOMContentLoaded', function() {
    const textArea = document.getElementById('answer_text');
    const wordCounter = document.getElementById('word_counter');
    const submitButton = document.querySelector('button[type="submit"]');
    
    if (textArea && wordCounter) {
        const wordLimit = parseInt(wordCounter.getAttribute('data-limit')) || 500;
        
        function updateWordCount() {
            // Count words (split by whitespace and filter out empty strings)
            const text = textArea.value.trim();
            const wordCount = text ? text.split(/\s+/).filter(Boolean).length : 0;
            
            // Update counter display
            wordCounter.textContent = `${wordCount} / ${wordLimit} words`;
            
            // Apply styling based on word count
            if (wordCount > wordLimit) {
                wordCounter.className = 'word-counter danger';
                if (submitButton) submitButton.disabled = true;
            } else if (wordCount > wordLimit * 0.9) {
                wordCounter.className = 'word-counter warning';
                if (submitButton) submitButton.disabled = false;
            } else {
                wordCounter.className = 'word-counter';
                if (submitButton) submitButton.disabled = false;
            }
        }
        
        // Initial count
        updateWordCount();
        
        // Add event listeners for typing and pasting
        textArea.addEventListener('input', updateWordCount);
        textArea.addEventListener('paste', function() {
            // Use setTimeout to ensure paste content is in the textarea
            setTimeout(updateWordCount, 10);
        });
    }
});
