// Function to update the question based on the selected choice
function updateQuestion() {
    // Get the selected option value
    const selectedChoice = document.getElementById("choices").value;

    // Make an AJAX request to the server to fetch the first question of the selected type
    $.ajax({
        url: '/question-by-type',
        method: 'GET',
        data: {
            type: selectedChoice
        },
        success: function(data) {
            // Update the content div with the image and description from the server
            const contentDiv = document.getElementById("question");
            // Clear the current content
            contentDiv.innerHTML = '';

            // Add the question image
            const questionImage = document.createElement('img');
            questionImage.src = data.image_url;
            questionImage.alt = 'Question Image';
            contentDiv.appendChild(questionImage);

            // Optionally, display any description or additional information provided by the server
            if (data.description) {
                const description = document.createElement('p');
                description.textContent = data.description;
                contentDiv.appendChild(description);
            }

            // Store the current question ID for later use
            currentQuestionId = data.id;

            // Clear the textbox and feedback div
            $('#answer').val(''); // Clear the textbox
            $('#feedback').text(''); // Clear the feedback div
        },
        error: function(error) {
            console.error('Error fetching question by type:', error);
            alert('An error occurred. Please try again later.');
        }
    });
}

$(document).ready(function() {
    // Event listener for dropdown menu change
    $('#choices').on('change', updateQuestion);

    // Automatically display the first "helper" type question when the page loads
    $('#choices').val('helper'); // Set the dropdown value to 'helper'
    updateQuestion(); // Call the function to update the question

    
    // Event listener for form submission
    $('#answerForm').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        $('#correction').text('');
        // Get the user's answer from the input field
        const userAnswer = $('#answer').val().trim();
    
        // Make an AJAX request to the server to check the user's answer
        $.ajax({
            url: '/check-answer',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                questionId: currentQuestionId,
                userAnswer: userAnswer
            }),
            success: function(response) {
                // Display feedback based on the server's response
                const feedbackDiv = $('#feedback');
                if (response.correct) {
                    feedbackDiv.text('Correct!');
                } else {
                    feedbackDiv.text('Wrong');
                    // Populate the correction div with the explanation for incorrect answer
                    $('#correction').text(response.explanation);
                }
            },
            error: function(error) {
                console.error('Error checking answer:', error);
                alert('An error occurred. Please try again later.');
            }
        });
    });
    
    // Event listener for the "Complete" button click
        $('#complete').on('click', function(event) {
            event.preventDefault(); // Prevent the default action (navigation)
            
            // Redirect the user to the /results page
            window.location.href = '/results';
        });

    // Event listener for the "Next Image" button click
    $('#nextImage').on('click', function(event) {
        event.preventDefault(); // Prevent the default action (navigation)
        
        $('#answer').val(''); 
        $('#feedback').text(''); 
        $('#correction').text('');

        // Make an AJAX request to the server to get the next question image
        $.ajax({
            url: '/next-question-image',
            method: 'GET',
            success: function(data) {
                // Update the question div with the next question image and description
                const contentDiv = $('#question');
                contentDiv.html(''); // Clear current content
    
                // Create an img element for the question image
                const questionImage = $('<img>', {
                    src: data.image_url,
                    alt: 'Next Question'
                });
    
                // Append the question image to the content div
                contentDiv.append(questionImage);
    
                // If there is any description provided in the response, append it
                if (data.description) {
                    const description = $('<p>').text(data.description);
                    contentDiv.append(description);
                }
    
                // Update the current question ID immediately after receiving the response
                currentQuestionId = data.id;
                console.log(currentQuestionId);
    
                // Check if the current question ID is 8
                if (currentQuestionId === 8) {
                    $('#nextImage').hide();
                    $('#complete').show();
                }
            },
            error: function(error) {
                console.error('Error fetching next question image:', error);
                alert('An error occurred. Please try again later.');
            }
        });
    });
});