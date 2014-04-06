Ext.require(['Ext.data.*', 'Ext.grid.*']);

Ext.define('ActivitySkill', {
    extend: 'Ext.data.Model',
    fields:
    [
        {
            name: 'activityID',
            type: 'int',
            useNull: true
        },
        {
            name: 'id',
            type: 'int',
            useNull: true
        },
        {
            name: 'category',
            type: 'string',
            useNull: true
        },
        {
            name: 'skill',
            type: 'string',
            useNull: true
        },
        {
            name: 'quantity',
            type: 'string'
        },
        'quantity',
        //'status',
        //'invitee',
        //'invitee status'
    ],
    validations:
    [
        {
            type: 'length',
            field: 'category',
            min: 1
        },
        {
            type: 'length',
            field: 'skill',
            min: 1
        }
    ]
    /*
    proxy:
    {
        type: 'rest',
        url: '/activity_ds/activitySkills.json?activityID' + talent_match_global['activityID']
    }
    */
});

Ext.onReady(function(){

    var sampleData =
        {"message": "Loaded data", "data": [{"category": "Software", "exclusivePerson": true, "activityID": 1, "categoryID": 6, "skill": "Python", "quantity": 1, "id": 1, "skillID": 32}, {"category": "Software", "exclusivePerson": true, "activityID": 1, "categoryID": 6, "skill": "HTML5", "quantity": 1, "id": 2, "skillID": 29}], "success": true};

    var store = Ext.create('Ext.data.Store', {
        autoLoad: true,
        autoSync: true,
        model: 'ActivitySkill',
        /*data : sampleData,
        proxy:
        {
            type: 'memory',
            reader: {
                type: 'json',
                root: 'data'
            }
        },
        */
        onCreateRecords: function(records, operation, success) {
            console.log(records);
        },

        onUpdateRecords: function(records, operation, success) {
            console.log(records);
        },

        onDestroyRecords: function(records, operation, success) {
            console.log(records);
        },

        proxy:
        {
            type: 'rest',

            pageParam: false, //to remove param "page"
            startParam: false, //to remove param "start"
            limitParam: false,

            // The activity ID is set on the page load in a simple script where the Jinja2 engine substitutes
            // the desired value.
            //url: '/activity/activitySkills.json?activityID' + talent_match_global['activityID'],
            url: '/activity_ds/activitySkills/',
            extraParams:
                {
                    activityID : talent_match_global['activityID']
                },
            reader:
            {
                type: 'json',
                idProperty: 'id',               //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                messageProperty: 'message',     //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                root: 'data',
                model : 'ActivitySkill'
            },
            writer:
            {
                type: 'json'
            }
        },
        listeners: {
            write: function(store, operation){
                var record = operation.getRecords()[0],
                    name = Ext.String.capitalize(operation.action),
                    verb;


                if (name == 'Destroy') {
                    record = operation.records[0];
                    verb = 'Destroyed';
                } else {
                    verb = name + 'd';
                }
                Ext.example.msg(name, Ext.String.format("{0} ActivitySkill: {1}", verb, record.getId()));

            }
        }
    });

    var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
        listeners: {
            cancelEdit: function(rowEditing, context) {
                // Canceling editing of a locally added, unsaved record: remove it
                if (context.record.phantom) {
                    store.remove(context.record);
                }
            }
        }
    });

    var grid = Ext.create('Ext.grid.Panel', {
        // trying to move this around ...
        // renderTo: document.body,
        renderTo: 'skill-panel',
        plugins: [rowEditing],
        width: 600,
        height: 400,
        frame: false,
        title: 'Add/Edit Skills',
        store: store,
        iconCls: 'icon-user',
        columns:
        [
            {
                text: 'ID',
                width: 40,
                sortable: true,
                dataIndex: 'id'
            },
            {
                text: 'Category',
                flex: 1,
                sortable: true,
                dataIndex: 'category',
                field: {
                    xtype: 'textfield'
                }
            },
            {
                header: 'Skill',
                flex: 1,
                // width: 80,
                sortable: true,
                dataIndex: 'skill',
                field: {
                    xtype: 'textfield'
                }
            },
            {
                text: 'Quantity',
                width: 80,
                sortable: true,
                dataIndex: 'quantity',
                field: {
                    xtype: 'textfield'
                }
            }
        ],
        dockedItems: [{
            xtype: 'toolbar',
            items: [{
                text: 'Add',
                iconCls: 'icon-add',
                handler: function(){
                    // empty record
                    store.insert(0, new ActivitySkill());
                    rowEditing.startEdit(0, 0);

                    // get the selection model in order to get which record is selected
                    //var sm = grid.getSelectionModel();

                    // after user clicks off from editing, sync the store, remove the record from the top and reload the store to see new changes
                    //grid.on('edit', function() {
                    //    var record = sm.getSelection()
                    //    store.sync();
                    //    store.remove(record);
                    //    store.load();
                    //});
                }
            }, '-', {
                itemId: 'delete',
                text: 'Delete',
                iconCls: 'icon-delete',
                disabled: true,
                handler: function(){
                    var selection = grid.getView().getSelectionModel().getSelection()[0];
                    if (selection) {
                        store.remove(selection);
                    }
                }
            }]
        }]
    });

    grid.getSelectionModel().on('selectionchange', function(selModel, selections){
        grid.down('#delete').setDisabled(selections.length === 0);
    });
});
