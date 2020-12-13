// check if the browser already has a value for 'counter', if not, set
if (!localStorage.getItem('counter')) {
  localStorage.setItem('counter', 0);
}

function count() {
  let counter = localStorage.getItem('counter');
  counter++;
  document.querySelector('h1').innerHTML = counter;
  localStorage.setItem('counter', counter);

  if (counter % 10 === 0) {
    alert(`Count is now ${counter}`);
  }
}

// wait until the content of the DOM has loaded, otherwise button doesn't exist
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('h1').innerHTML = localStorage.getItem('counter');
  document.querySelector('button').onclick = count;
  // or increment every 1000 milliseconds
  // setInterval(count, 1000);
});
