const cgpaOptions = document.querySelectorAll('#cgpa .dropdown-item');

cgpaOptions.forEach(option => {
  option.addEventListener('click', function() {
    handleSelection(this.id, 'cgpa');
  });
});

function handleSelection(selectedOption, selectType) {
  // Code to handle the selection of any option

  const options = {
    cgpa: ['a', 'b', 'c', 'd']
  };

  // Remove the 'active' class from all options
  options[selectType].forEach(option => {
    document.getElementById(option).classList.remove('active');
  });

  // Add the 'active' class to the selected option
  document.getElementById(selectedOption).classList.add('active');

  // You can perform any necessary actions or call functions here
}
