function sendEmail(messageOnSuccess) {
  // Get data from fields
  const name = document.querySelector("form > div > input#name").value;
  const email = document.querySelector("form > div > input#email").value;
  const message = document.querySelector("form > div > textarea#message").value;
  // Data validation
  if (email == "" || message == "") return true;
  // Set up request
  const formData = new FormData();
  formData.append("name", name);
  formData.append("_replyto", email);
  formData.append("message", message);

  const plainFormData = Object.fromEntries(formData.entries());
  const formDataJsonString = JSON.stringify(plainFormData);

  // Send request
  fetch("https://formspree.io/f/xpzkroqj", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    redirect: "manual",
    body: formDataJsonString,
  }).then(() => {
    // Show success message
    alert(messageOnSuccess);
  });

  return false;
}
