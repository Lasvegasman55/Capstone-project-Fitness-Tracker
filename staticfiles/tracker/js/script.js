// FitTrack Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Function to handle dynamic form fields for workout exercises
    setupExerciseFormset();

    // Setup exercise search functionality
    setupExerciseSearch();

    // Setup chart rendering if on analytics page
    if (document.getElementById('weightChart')) {
        renderWeightChart();
    }
    
    if (document.getElementById('nutritionChart')) {
        renderNutritionChart();
    }
    
    if (document.getElementById('exerciseChart')) {
        renderExerciseChart();
    }

    // Handle date picker changes for filtering data
    setupDateFilters();
});

// Function to handle workout exercise formset
function setupExerciseFormset() {
    const addExerciseBtn = document.getElementById('add-exercise-btn');
    if (addExerciseBtn) {
        addExerciseBtn.addEventListener('click', function() {
            const formsetContainer = document.getElementById('exercise-formset');
            const forms = formsetContainer.querySelectorAll('.exercise-form');
            const totalFormsInput = document.getElementById('id_exercises-TOTAL_FORMS');
            
            // Clone the first form
            const newForm = forms[0].cloneNode(true);
            
            // Update form index
            const formCount = forms.length;
            newForm.innerHTML = newForm.innerHTML.replace(/-0-/g, `-${formCount}-`);
            
            // Clear values in the cloned form
            newForm.querySelectorAll('input, select, textarea').forEach(input => {
                // Don't clear hidden fields like csrf token
                if (input.type !== 'hidden' || input.name.includes('exercises')) {
                    if (input.type === 'checkbox') {
                        input.checked = false;
                    } else {
                        input.value = '';
                    }
                }
            });
            
            // Increment the form count
            totalFormsInput.value = formCount + 1;
            
            // Add the new form to the container
            formsetContainer.appendChild(newForm);
            
            // Re-initialize any special inputs in the new form
            setupExerciseSearch();
        });
    }
}

// Function to setup exercise search
function setupExerciseSearch() {
    const exerciseSearchInputs = document.querySelectorAll('.exercise-search');
    
    exerciseSearchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const exerciseSelect = this.closest('.form-group').querySelector('select');
            
            if (exerciseSelect) {
                const options = exerciseSelect.querySelectorAll('option');
                
                options.forEach(option => {
                    const optionText = option.textContent.toLowerCase();
                    const optionValue = option.value;
                    
                    // Skip the empty/default option
                    if (optionValue === '') return;
                    
                    if (optionText.includes(searchTerm)) {
                        option.style.display = '';
                    } else {
                        option.style.display = 'none';
                    }
                });
            }
        });
    });
}

// Function to render weight chart on analytics page
function renderWeightChart() {
    const ctx = document.getElementById('weightChart').getContext('2d');
    
    // This will be populated by Django template
    const weightData = JSON.parse(document.getElementById('weight-data').textContent || '[]');
    
    if (weightData.length > 0) {
        const labels = weightData.map(item => item.date);
        const weights = weightData.map(item => item.weight);
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Weight (kg)',
                    data: weights,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    tension: 0.2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Weight Progress Over Time'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Weight (kg)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }
}

// Function to render nutrition chart on analytics page
function renderNutritionChart() {
    const ctx = document.getElementById('nutritionChart').getContext('2d');
    
    // This will be populated by Django template
    const nutritionData = JSON.parse(document.getElementById('nutrition-data').textContent || '[]');
    
    if (nutritionData.length > 0) {
        const labels = nutritionData.map(item => item.date);
        const calories = nutritionData.map(item => item.daily_calories);
        const protein = nutritionData.map(item => item.daily_protein);
        const carbs = nutritionData.map(item => item.daily_carbs);
        const fat = nutritionData.map(item => item.daily_fat);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Calories (kcal)',
                        data: calories,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgb(255, 99, 132)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Protein (g)',
                        data: protein,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgb(54, 162, 235)',
                        borderWidth: 1,
                        yAxisID: 'y1'
                    },
                    {
                        label: 'Carbs (g)',
                        data: carbs,
                        backgroundColor: 'rgba(255, 206, 86, 0.7)',
                        borderColor: 'rgb(255, 206, 86)',
                        borderWidth: 1,
                        yAxisID: 'y1'
                    },
                    {
                        label: 'Fat (g)',
                        data: fat,
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgb(75, 192, 192)',
                        borderWidth: 1,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Nutrition Intake Over Time'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Calories (kcal)'
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Macros (g)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
}

// Function to render exercise chart on analytics page
function renderExerciseChart() {
    const ctx = document.getElementById('exerciseChart').getContext('2d');
    
    // This will be populated by Django template
    const exerciseData = JSON.parse(document.getElementById('exercise-data').textContent || '[]');
    
    if (exerciseData.length > 0) {
        const labels = exerciseData.map(item => item.exercise__name);
        const counts = exerciseData.map(item => item.count);
        
        new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Frequency',
                    data: counts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(199, 199, 199, 0.7)',
                        'rgba(83, 102, 255, 0.7)',
                        'rgba(40, 159, 64, 0.7)',
                        'rgba(210, 99, 132, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    title: {
                        display: true,
                        text: 'Most Frequent Exercises'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Sets'
                        }
                    }
                }
            }
        });
    }
}

// Setup date filters for various lists
function setupDateFilters() {
    const dateFilter = document.getElementById('date-filter');
    if (dateFilter) {
        dateFilter.addEventListener('change', function() {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('date', this.value);
            window.location.href = currentUrl.toString();
        });
    }

    const dateRangeStart = document.getElementById('date-range-start');
    const dateRangeEnd = document.getElementById('date-range-end');
    const applyDateRange = document.getElementById('apply-date-range');
    
    if (dateRangeStart && dateRangeEnd && applyDateRange) {
        applyDateRange.addEventListener('click', function() {
            const start = dateRangeStart.value;
            const end = dateRangeEnd.value;
            
            if (start && end) {
                const currentUrl = new URL(window.location.href);
                currentUrl.searchParams.set('start_date', start);
                currentUrl.searchParams.set('end_date', end);
                window.location.href = currentUrl.toString();
            }
        });
    }
}