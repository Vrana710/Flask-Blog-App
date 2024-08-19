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
    // Handle comment form submission
    $('.comment-form').on('submit', function(event) {
        event.preventDefault();
        
        const form = $(this);
        const postId = form.data('post-id');
        const formData = form.serialize();
        
        $.post(`/comment/${postId}`, formData, function(data) {
          // Clear existing comments
          const commentsList = $(`#post-${postId} .comments-list`);
          commentsList.empty();
          
          // Append new comments
          $.each(data.comments, function(index, comment) {
            commentsList.append(`
              <div class="comment">
                <p><strong>${comment.author}:</strong> ${comment.text}</p>
              </div>
            `);
          });
          
          // Clear the comment form
          form[0].reset();
        });
      });
    
      // Handle delete button click
      $('.delete-form').on('submit', function(event) {
        event.preventDefault();
        
        if (confirm('Are you sure you want to delete this post?')) {
          $(this).off('submit').submit();
        }
      });
  });
  