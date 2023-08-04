// JavaScript code for selectMajor dropdown selection
const stOption = document.getElementById('st');
const shOption = document.getElementById('sh');
const bmOption = document.getElementById('bm');
const otherOption = document.getElementById('other');

stOption.onclick = function() {
  handleSelection('st');
};
shOption.onclick = function() {
  handleSelection('sh');
};
bmOption.onclick = function() {
  handleSelection('bm');
};
otherOption.onclick = function() {
  handleSelection('other');
};

function handleSelection(selectedOption) {
  // Code to handle the selection of any option

  // Remove the 'active' class from all options
  stOption.classList.remove('active');
  shOption.classList.remove('active');
  bmOption.classList.remove('active');
  otherOption.classList.remove('active');

  // Add the 'active' class to the selected option
  document.getElementById(selectedOption).classList.add('active');

  // You can perform any necessary actions or call functions here
}
