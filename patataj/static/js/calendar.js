document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'pl',
        buttonText: {
            today: 'Dzisiaj',
            month: 'Miesiąc',
            week: 'Tydzień',
            day: 'Dzień',
            list: 'Lista'
        },
        events: calendarEvents,
        eventContent: function(arg) {
            let startTime = arg.event.start.toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit', hour12: false });
            let endTime = arg.event.end ? arg.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false }) : '';
            let title = arg.event.title;

            let content = document.createElement('div');
            content.innerHTML = '<b>' + startTime + ' - ' + endTime + '</b><br>' + title;
            return { domNodes: [content] };
        }
    });
    calendar.render();
});
