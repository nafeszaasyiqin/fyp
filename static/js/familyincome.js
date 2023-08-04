const familyIncomeOptions = document.querySelectorAll('#familyincome .dropdown-item');

familyIncomeOptions.forEach(option => {
  option.addEventListener('click', function() {
    handleSelection(this.id, 'familyIncome');
  });
});

function handleSelection(selectedOption, selectType) {
  // Code to handle the selection of any option

  const options = {
    familyIncome: ['b40', 'm40', 't20']
  };

  // Remove the 'active' class from all options
  options[selectType].forEach(option => {
    document.getElementById(option).classList.remove('active');
  });

  // Add the 'active' class to the selected option
  document.getElementById(selectedOption).classList.add('active');

  // You can perform any necessary actions or call functions here
}
