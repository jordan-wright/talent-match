$(document).ready(function() {
    var skills = new Bloodhound({
        datumTokenizer: function (d) { return Bloodhound.tokenizers.whitespace(d.value); },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        limit: 10,
        remote : {
        	url: '/skills/search?query=%QUERY',
        	filter: function (results) {
	            return $.map(results.skills, function (skill) {
	                return {
	                    value: skill.name
	                };
	            });
       		}
       	}
    });

    // kicks off the loading/processing of `local` and `prefetch`
    skills.initialize();
    $('#query').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    }, {
        name: 'skills',
        displayKey: 'value',
        source: skills.ttAdapter()
    });
});
