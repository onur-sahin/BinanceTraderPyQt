


// dateValidator.js


function onDateTextChanged(dateInput) {
    // console.log("Date validation triggered for: " + dateInput.text);

    // 1. Format doğrulama: Gün/ay/yıl formatı
    var datePattern = /^(0?[1-9]|[12][0-9]|3[01])\/(0?[1-9]|1[0-2])\/(19|20)\d\d$/;
    if (!datePattern.test(dateInput.text)) {
        dateInput.placeholderText = "Invalid date format";
        dateInput.color = "red";
        dateInput.font.bold = true;
        return false;  // Hatalı formatta ise işlemi sonlandır
    }

    // 2. Tarih formatı doğruysa, ayıklama yap
    var parts = dateInput.text.split('/');
    var day = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);

    // 3. Günün geçerli olup olmadığını kontrol et
    var daysInMonth = new Date(year, month, 0).getDate();
    if (day > daysInMonth) {
        dateInput.placeholderText = `Invalid day for month (${daysInMonth} days)`;
        dateInput.color = "red";
        dateInput.font.bold = true;
        return false;
    }

    // 4. Tüm kontroller geçti, geçerli tarih
    dateInput.color = dateInput.defaultColor;
    dateInput.font.bold = false;
    dateInput.placeholderText = "DD/MM/YYYY";

    return true;
}


function onTimeTextChanged(timeInput){
  
    // 1. Format doğrulama: HH:MM (24 saatlik format)
    var timePattern = /^(0?[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$/;
    if (!timePattern.test(timeInput.text)) {
        timeInput.placeholderText = "Invalid time format (HH:MM)";
        timeInput.color = "red";
        timeInput.font.bold = true;
        return false;  // Hatalı formatta ise işlemi sonlandır
    }

    // 2. Tüm kontroller geçti, geçerli saat
    timeInput.color = timeInput.defaultColor;
    timeInput.font.bold = false;
    timeInput.placeholderText = "HH:MM";

    return true;

}




