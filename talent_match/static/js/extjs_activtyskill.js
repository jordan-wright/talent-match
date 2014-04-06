Ext.require(['Ext.data.*', 'Ext.grid.*']);

Ext.define('Person', {
    extend: 'Ext.data.Model',
    fields: [{
        name: 'id',
        type: 'int',
        useNull: true
    }, 'email', 'first', 'last'],
    validations: [{
        type: 'length',
        field: 'email',
        min: 1
    }, {
        type: 'length',
        field: 'first',
        min: 1
    }, {
        type: 'length',
        field: 'last',
        min: 1
    }]
});

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
        'status',
        'invitee',
        'invitee status'
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
});

Ext.onReady(function(){
    var store = Ext.create('Ext.data.Store', {
        autoLoad: true,
        autoSync: true,
        model: 'ActivitySkill',
        proxy: {
            type: 'rest',
            // The activity ID is set on the page load in a simple script where the Jinja2 engine substitutes
            // the desired value.
            url: '/activity/activitySkills.json/?activityID=' + talent_match_global['activityID'],
            reader: {
                type: 'json',
                root: 'data'
            },
            writer: {
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
                Ext.example.msg(name, Ext.String.format("{0} activity skill: {1}", verb, record.getId()));

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
        renderTo: document.body,
        plugins: [rowEditing],
        width: 600,
        height: 400,
        frame: false,
        // title: 'Users',
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
                width: 80,
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

    /*
    var store = Ext.create('Ext.data.Store', {
        autoLoad: true,
        autoSync: true,
        model: 'Person',
        proxy: {
            type: 'rest',
            url: 'http://docs.sencha.com/extjs/4.2.1/extjs-build/examples/restful/app.php/users',
            reader: {
                type: 'json',
                root: 'data'
            },
            writer: {
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
                Ext.example.msg(name, Ext.String.format("{0} user: {1}", verb, record.getId()));

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
        renderTo: document.body,
        plugins: [rowEditing],
        width: 400,
        height: 300,
        frame: true,
        title: 'Users',
        store: store,
        iconCls: 'icon-user',
        columns: [{
            text: 'ID',
            width: 40,
            sortable: true,
            dataIndex: 'id'
        }, {
            text: 'Email',
            flex: 1,
            sortable: true,
            dataIndex: 'email',
            field: {
                xtype: 'textfield'
            }
        }, {
            header: 'First',
            width: 80,
            sortable: true,
            dataIndex: 'first',
            field: {
                xtype: 'textfield'
            }
        }, {
            text: 'Last',
            width: 80,
            sortable: true,
            dataIndex: 'last',
            field: {
                xtype: 'textfield'
            }
        }],
        dockedItems: [{
            xtype: 'toolbar',
            items: [{
                text: 'Add',
                iconCls: 'icon-add',
                handler: function(){
                    // empty record
                    store.insert(0, new Person());
                    rowEditing.startEdit(0, 0);
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
    */
});
