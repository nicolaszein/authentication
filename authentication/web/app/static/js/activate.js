document.addEventListener('DOMContentLoaded', function() {
  const urlParams = new URLSearchParams(window.location.search);
  const activationToken = urlParams.get('activation_token');
  const cta = document.getElementById("call-to-action");
  const loading = document.getElementById("loading");
  const initialContent = document.getElementById("initial-content");
  const errorContent = document.getElementById("error-content");
  const successContent = document.getElementById("success-content");

  cta.addEventListener("click", function(){
    toggleElements([initialContent, loading]);
    hideElement(errorContent);

    fetch(
      `${window.location.origin}/api/users/activate`,
      {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          activation_token: activationToken
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
