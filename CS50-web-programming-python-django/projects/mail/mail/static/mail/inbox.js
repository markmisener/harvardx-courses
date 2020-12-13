document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
  document.querySelector('#compose').addEventListener('click', displayComposeView);

  loadMailbox('inbox');
});

function clearFormFields() {
  // Clear composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function displayComposeView() {
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
}

function sendEmail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => {
    return response.json()
  })
  .then(result => {
    clearFormFields();
    loadMailbox('sent');
  })
  .catch(error => console.log(error));

  return false;
}

function loadMailbox(mailbox) {
  // Load a mailbox
  const emailsView = document.querySelector('#emails-view')
  clearFormFields();

  // Display the emails-view div and hide others
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    if (emails.length > 0) {
      emails.forEach(email => {
        const emailCard = document.createElement('div');
        emailCard.innerHTML = `
            <div id="emails-card" data-read=${email.read}>
              <p>${email.sender}</p>
              <p>${email.timestamp}</p>
              <p>${email.subject}</p>
            </div>
        `

        emailCard.addEventListener('click', () => {
          // Mark email as read
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          loadEmail(email.id);
        });

        emailsView.appendChild(emailCard);
      });
    } else {
      // No emails in mailbox
      const emailCard = document.createElement('div');
      emailCard.className = "emails-card";
      emailCard.innerHTML = `There are no emails in your ${mailbox}.`;
      emailsView.appendChild(emailCard);
    }
  })
  .catch(error => console.log(error));
}

function loadEmail(emailId) {
  // Load an email by id
  const emailView = document.querySelector('#email-view');
  // Remove existing children on a given div
  while (emailView.firstChild) {
    emailView.removeChild(emailView.lastChild);
  }

  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Fetch email by ID
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    const emailItem = document.createElement('div');
    emailItem.innerHTML = `
      <div id="email-card" data-read=${email.read}>
        <div id="email-header">
          <strong><p>${email.sender}</p></strong>
          <p>To: ${email.recipients} | ${email.timestamp}</p>
          <p>${email.subject}</p>
        </div>
        <div id="email-body">
          ${email.body}
        </div>
      </div>
    `
    // Add archive button
    var archiveInputElement = document.createElement('input');
    archiveInputElement.type = "button";

    if (email.archived === false) {
      archiveInputElement.value = "Archive";
    } else {
      archiveInputElement.value = "Unarchive";
    };

    archiveInputElement.addEventListener('click', function() {
      toggleArchiveEmail(email);
      loadMailbox('inbox');
    });

    // Add reply button
    var replyInputElement = document.createElement('input');
    replyInputElement.type = "button";
    replyInputElement.value = "Reply";
    replyInputElement.addEventListener('click', function() {
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      const subject = (email.subject.startsWith("Re:")) ? email.subject : `Re: ${email.subject}`;
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}`;
      displayComposeView();
    });

    emailItem.appendChild(archiveInputElement);
    emailItem.appendChild(replyInputElement);
    emailView.appendChild(emailItem);
  })
  .catch(error => console.log(error));
}

function toggleArchiveEmail(email) {
  // Toggle if an email is archived
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  })
}
