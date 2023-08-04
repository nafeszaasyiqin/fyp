// JavaScript code for selectMajor dropdown selection
const foundationoption = document.getElementById('foundation');
const diplomaoption = document.getElementById('diploma');
const degreeoption = document.getElementById('degree');
const masteroption = document.getElementById('master');
const phdoption = document.getElementById('phd');

foundationoption.onclick = function() {
  handleSelection('foundation');
};
diplomaoption.onclick = function() {
  handleSelection('diploma');
};
degreeoption.onclick = function() {
  handleSelection('degree');
};
masteroption.onclick = function() {
  handleSelection('master');
};
phdoption.onclick = function() {
  handleSelection('phd');
};

function handleSelection(selectedOption) {
  // Code to handle the selection of any option

  // Remove the 'active' class from all options
 foundationoption.classList.remove('active');
  diplomaoption.classList.remove('active');
  degreeoption.classList.remove('active');
  masteroption.classList.remove('active');
  phdoption.classList.remove('active');

  // Add the 'active' class to the selected option
  document.getElementById(selectedOption).classList.add('active');

  // You can perform any necessary actions or call functions here
}
