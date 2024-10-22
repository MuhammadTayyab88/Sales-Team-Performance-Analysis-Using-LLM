
$(document).ready(function () {
    // Show employee dropdown when clicking the button
    $('#selectEmployeeBtn').click(function () {
        $('#employeeDropdown').toggle();
    });

    // Load available dates when an employee is selected
    $('#employeeDropdown').change(function () {
        const employeeName = encodeURIComponent($('#employeeDropdown').val());

        if (employeeName) {
            $('#loadingSpinner').show(); // Show spinner while loading dates

            // Fetch available dates for the selected employee
            $.ajax({
                url: `/api/individual_performance/${employeeName}`,
                type: 'GET',
                success: function (response) {
                    $('#loadingSpinner').hide(); // Hide spinner after loading

                    if (response.available_dates && response.available_dates.length > 0) {
                        $('#dateDropdown').empty(); // Clear previous dates
                        $('#dateDropdown').append('<option value="">Select Date</option>');

                        response.available_dates.forEach(function (date) {
                            $('#dateDropdown').append(`<option value="${date}">${date}</option>`);
                        });

                        $('#dateDropdown').show(); // Show date dropdown
                        $('#fetchPerformanceBtn').show(); // Show fetch button
                    } else {
                        alert('No available dates for this employee.');
                    }
                },
                error: function (xhr, status, error) {
                    $('#loadingSpinner').hide(); // Hide spinner on error
                    alert('Failed to fetch available dates.');
                    console.error('Error:', error);
                }
            });
        } else {
            $('#dateDropdown').hide();
            $('#fetchPerformanceBtn').hide();
            alert('Please select an employee.');
        }
    });

    // Fetch performance data when a date is selected
    $('#fetchPerformanceBtn').click(function () {
        const selectedDate = $('#dateDropdown').val();
        const employeeName = encodeURIComponent($('#employeeDropdown').val());

        if (selectedDate && employeeName) {
            $('#loadingSpinner').show(); // Show spinner during data loading

            // Fetch performance data for the selected employee and date
            $.ajax({
                url: `/api/individual_performance/${employeeName}/?selected_date=${selectedDate}`,
                type: 'GET',
                success: function (response) {
                    $('#loadingSpinner').hide(); // Hide spinner after loading
            
                    if (response.insights) {
                        const data = response.insights;
                        $('#repName').text(decodeURIComponent(employeeName)); // Display employee name
            
                        // Display main performance data
                        $('#individualTotalLeads').text(data.total_leads_taken ?? 'N/A');
                        $('#individualTotalTours').text(data.total_tours_booked ?? 'N/A');
                        $('#individualTotalApplications').text(data.total_applications ?? 'N/A');
            
                        // Display text messages sent
                        const textMessages = data.total_text_messages_sent || {};
                        $('#individualMonText').text(textMessages.Mon ?? 'N/A');
                        $('#individualTueText').text(textMessages.Tue ?? 'N/A');
                        $('#individualWedText').text(textMessages.Wed ?? 'N/A');
                        $('#individualThuText').text(textMessages.Thu ?? 'N/A');
                        $('#individualFriText').text(textMessages.Fri ?? 'N/A');
                        $('#individualSatText').text(textMessages.Sat ?? 'N/A');
                        $('#individualSunText').text(textMessages.Sun ?? 'N/A');
            
                        // Display calls made
                        const callsMade = data.total_calls_made || {};
                        $('#individualMonCall').text(callsMade.Mon ?? 'N/A');
                        $('#individualTueCall').text(callsMade.Tue ?? 'N/A');
                        $('#individualWedCall').text(callsMade.Wed ?? 'N/A');
                        $('#individualThuCall').text(callsMade.Thu ?? 'N/A');
                        $('#individualFriCall').text(callsMade.Fri ?? 'N/A');
                        $('#individualSatCall').text(callsMade.Sat ?? 'N/A');
                        $('#individualSunCall').text(callsMade.Sun ?? 'N/A');
            
                        // Show the performance table
                        $('#performanceTable').show();
                    } else {
                        alert('No data available for this employee on the selected date.');
                    }
                },
                error: function (xhr, status, error) {
                    $('#loadingSpinner').hide(); // Hide spinner on error
                    alert('Failed to fetch performance data.');
                    console.error('Error:', error);
                }
            });
            
        } else {
            alert('Please select both an employee and a date.');
        }
    });
});


$(document).ready(function() {
    // Fetch performance data when the button is clicked
    $('#fetchPerformanceTrendsBtn').click(function() {
        const fromDate = $('#fromDate').val();
        const toDate = $('#toDate').val();

        // Check if both dates are provided
        if (!fromDate || !toDate) {
            $('#errorMessage').text("Both 'from' and 'to' dates are required.").show();
            return;
        }

        // Ensure fromDate is earlier or equal to toDate
        if (fromDate > toDate) {
            $('#errorMessage').text("'From' date cannot be later than 'To' date.").show();
            return;
        }

        // Hide error message if validation passes
        $('#errorMessage').hide();

        // Show spinner and hide the table while fetching data
        showSpinner();
        $('#monthlyTrendsTable').hide();

        // Fetch the performance trends data
        $.ajax({
            url: `/api/performance_trends/?from_date=${fromDate}&to_date=${toDate}`,
            type: 'GET',
            success: function(response) {
                console.log("Monthly Performance Trends Response: ", response);

                if (response.error) {
                    alert(response.error);  // Display any errors from the backend
                    return;
                }

                // Populate the table with performance data
                const data = response.performance_trends_summary;
                let tableBody = '';
                tableBody += `<tr>
                    <td>Selected Range</td>
                    <td>${data.total_leads_taken}</td>
                    <td>${data.total_tours_booked}</td>
                    <td>${data.total_applications}</td>
                </tr>`;

                // Insert the rows into the table body and show the table
                $('#monthlyTrendsBody').html(tableBody);
                hideSpinner();
                $('#monthlyTrendsTable').show();
            },
            error: function(xhr, status, error) {
                console.error("Error fetching performance trends:", error);
                alert('Failed to fetch performance trends.');
                hideSpinner();
            }
        });
    });

    // Utility functions for showing and hiding the spinner
    function showSpinner() {
        $('#loadingSpinner').show();
    }

    function hideSpinner() {
        $('#loadingSpinner').hide();
    }
});




// Fetch team performance when a team is selected from the dropdown
$('#getTeamPerformanceBtn').click(function() {
    $('#teamDropdown').toggle();  // Show/Hide team dropdown
});

$('#teamDropdown').change(function() {
    const teamName = $(this).val();  // Get the selected team name
    if (!teamName) {
        alert('Please select a team to view its performance.');
        return;
    }

    showSpinner();  // Show spinner while fetching
    $('#teamPerformanceTable').hide();  // Hide the performance table while loading

    // AJAX call to fetch the team performance data
    $.ajax({
        url: `/api/team_performance/?team_name=${teamName}`,
        method: 'GET',
        success: function(response) {
            const teamData = response.team_insights;
    
            if (teamData) {
                // Populate the performance table
                $('#teamTotalLeads').text(teamData.total_leads_taken || 'N/A');
                $('#teamTotalTours').text(teamData.total_tours_booked || 'N/A');
                $('#teamTotalApplications').text(teamData.total_applications || 'N/A');
    
                // Handle conversion ratios safely
                if (teamData.conversion_ratios) {
                    $('#teamToursPerLead').text(teamData.conversion_ratios.tours_per_lead ? teamData.conversion_ratios.tours_per_lead.toFixed(2) : 'N/A');
                    $('#teamAppsPerTour').text(teamData.conversion_ratios.apps_per_tour ? teamData.conversion_ratios.apps_per_tour.toFixed(2) : 'N/A');
                    $('#teamAppsPerLead').text(teamData.conversion_ratios.apps_per_lead ? teamData.conversion_ratios.apps_per_lead.toFixed(2) : 'N/A');
                }
    
                // Populate the text messages table
                const textMessages = teamData.total_text_messages_sent;
                $('#teamMonText').text(textMessages.Mon || 'N/A');
                $('#teamTueText').text(textMessages.Tue || 'N/A');
                $('#teamWedText').text(textMessages.Wed || 'N/A');
                $('#teamThuText').text(textMessages.Thu || 'N/A');
                $('#teamFriText').text(textMessages.Fri || 'N/A');
                $('#teamSatText').text(textMessages.Sat || 'N/A');
                $('#teamSunText').text(textMessages.Sun || 'N/A');
    
                // Populate the calls table
                const callsMade = teamData.total_calls_made;
                $('#teamMonCall').text(callsMade.Mon || 'N/A');
                $('#teamTueCall').text(callsMade.Tue || 'N/A');
                $('#teamWedCall').text(callsMade.Wed || 'N/A');
                $('#teamThuCall').text(callsMade.Thu || 'N/A');
                $('#teamFriCall').text(callsMade.Fri || 'N/A');
                $('#teamSatCall').text(callsMade.Sat || 'N/A');
                $('#teamSunCall').text(callsMade.Sun || 'N/A');
    
                // Show the performance tables
                hideSpinner();
                $('#teamPerformanceTable').show();
            } else {
                console.error("No team insights available.");
                alert('No data available for this team.');
                hideSpinner();
            }
        },
        error: function() {
            alert('Error fetching team performance.');
            hideSpinner();  // Hide spinner on failure
        }
    });        
    
    
});

// Utility functions for showing and hiding the spinner
function showSpinner() {
    $('#loadingSpinner').show();  // Show the spinner
}

function hideSpinner() {
    $('#loadingSpinner').hide();  // Hide the spinner
}
