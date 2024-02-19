function notification_trigger($title, $text){
    
    // Create notification with close button
    var notification = app.notification.create({
      icon: '<img src="/Secure_Coding/Resources/GoldwardFinancial/Images/favicon.ico">',
      title: '<p style="color: darkred">Goldward Financial: Secure Coding</p>',
      subtitle: $title,
      text: $text,
      closeButton: true,
    });
    
    notification.open();
}

function notification_trigger_ba($title, $text){
    
    // Create notification with close button
    var notification = app.notification.create({
      icon: '<img src="/Secure_Coding/Resources/LeekChef/leek.png">',
      title: '<p style="color: darkorange">Leek Chef: Broken Authentication</p>',
      subtitle: $title,
      text: $text,
      closeButton: true,
    });
    
    notification.open();
}
