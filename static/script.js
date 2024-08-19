$(document).ready(function() {
    $('.like-btn').on('click', function(event) {
      event.preventDefault(); // Prevent the default form submission
  
      var button = $(this);
      var postId = button.data('post-id');
      
      $.ajax({
        url: '/like/' + postId,
        type: 'POST',
        success: function(response) {
          // Update the like count
          button.find('.like-count').text(response.likes);
        },
        error: function(xhr, status, error) {
          console.error('Error:', error);
        }
      });
    });
  });
  