document.addEventListener('DOMContentLoaded', function() {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get('token');
  const resetPasswordForm = document.getElementById("reset-password-form");
  const confirmationPasswordError = document.getElementById("error-password-confirmation");
  const loading = document.getElementById("loading");
  const initialContent = document.getElementById("initial-content");
  const errorContent = document.getElementById("error-content");
  const successContent = document.getElementById("success-content");

  resetPasswordForm.addEventListener("submit", function(e){
    e.preventDefault();

    const password = document.getElementsByName("password")[0].value;
    const confirmationPassword = document.getElementsByName("confirmation_password")[0].value;

    if(password !== confirmationPassword) {
      toggleElement(confirmationPasswordError);

      return false;
    };

    toggleElements([initialContent, loading]);
    hideElement(errorContent);
    hideElement(confirmationPasswordError);

    fetch(
      `${window.location.origin}/api/reset-password/${token}`,
      {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          password: password
        })
      }
    ).then(
      function(res){
        if (res.ok) {
          toggleElements([loading, successContent]);
        } else {
          setTimeout(function(){
            toggleElements([errorContent, loading, initialContent]);
          }, 500);
        }
      }
    );
  });
});
