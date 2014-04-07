Ext.require(['Ext.data.*', 'Ext.grid.*']);

Ext.define('Category', {
    extend: 'Ext.data.Model',
    fields:
    [
        {
            name: 'id',
            type: 'int'
        },
        {
            name: 'name',
            type: 'string'
        }
    ]
});

Ext.define('Skill', {
    extend: 'Ext.data.Model',
    fields:
    [
        {
            name: 'id',
            type: 'int'
        },
        {
            name: 'name',
            type: 'string'
        }
    ]
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
            name: 'categoryID',
            type: 'integer',
            useNull: true
        },
        {
            name: 'skill',
            type: 'string',
            useNull: true
        },
        {
            name: 'skillID',
            type: 'integer',
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

    var  categoryListStore =Ext.create('Ext.data.Store', {
        autoLoad: true,
        model: 'Category',
        proxy:
        {
            type: 'rest',
            pageParam: false, //to remove param "page"
            startParam: false, //to remove param "start"
            limitParam: false,
            // The activity ID is set on the page load in a simple script where the Jinja2 engine substitutes
            // the desired value.
            //url: '/activity/activitySkills.json?activityID' + talent_match_global['activityID'],
            url: '/categories_ds/categories.json',
            reader:
            {
                type: 'json',
                idProperty: 'id',               //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                messageProperty: 'message',     //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                root: 'data',
                model : 'Category'
            },
            writer:
            {
                type: 'json'
            }
        }
    });

    /*
    var  skillListStore =Ext.create('Ext.data.Store', {
        autoLoad: true,
        model: 'Skill',
        proxy:
        {
            type: 'rest',
            pageParam: false, //to remove param "page"
            startParam: false, //to remove param "start"
            limitParam: false,
            url: '/skill_ds/skills.json',
            extraParams: {
                id: 1
            },
            reader:
            {
                type: 'json',
                idProperty: 'id',               //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                messageProperty: 'message',     //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                root: 'data',
                model : 'Skill'
            },
            writer:
            {
                type: 'json'
            }
        }
    });
*/

    var  skillListStoreBad =Ext.create('Ext.data.Store', {
        autoLoad: true,
        model: 'Skill',
            type: 'rest',
            pageParam: false, //to remove param "page"
            startParam: false, //to remove param "start"
            limitParam: false,
            // The activity ID is set on the page load in a simple script where the Jinja2 engine substitutes
            // the desired value.
            //url: '/activity/activitySkills.json?activityID' + talent_match_global['activityID'],
            url: '/skills_ds/skills.json',
            extraParams: {
                id: 1   // This will need to be replaced in later calls.
            },
            reader:
            {
                type: 'json',
                idProperty: 'id',               //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                messageProperty: 'message',     //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                root: 'data',
                model : 'Skill'
            },
            writer:
            {
                type: 'json'
            }
        });

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
                    xtype: 'combobox',
                    typeAhead : true,
                    triggerAction: 'all',
                    selectOnTab: true,
                    queryCaching : false,
                    // store: [ 'Music', 'Software', 'Golf'],  // need to replace this.
                    store: categoryListStore,
                    emptyText: 'Select a Category',
                    valueField : 'name',
                    displayField : 'name',
                    id : 'combo-select-category-id',
                    // lazyRender: true,
                    listClass: 'x-combo-list-medium',
                    listeners: {
                        'change' : function(field,nval,oval) {
                            console.log('Fired category changed event; trying to load the selection for the skill list.');
                            // No idea what this does.
                            // t.record.set('skill', '0');
                        },
                        'select' : function(field,nval,oval) {
                            console.log('Fired category selected event; trying to load the selection for the skill list.');
                            // console.log('new value 1:' + JSON.stringify(nval));
                            var selectedItem = null;
                            var previousItem = null;
                            // extraParms = {'id':selectedItem.id };
                            if ((Array.isArray(nval)) && (nval.length > 0)) {
                                selectedItem = nval[0].data;
                            }
                            if ((Array.isArray(oval)) && (oval.length > 0)) {
                                previousItem = oval[0].data;
                            }
                            if (previousItem !== selectedItem) {
                                var skillCombo = Ext.get('combo-select-skill-id');
                                if (skillCombo) {
                                    skillCombo.clearValue()
                                    skillListStore.extraParams = {'id':selectedItem.id };
                                    skillListStore.reload();
                                }
                            }
                        }
                    }
                }
            },
            {
                header: 'Skill',
                flex: 1,
                // width: 80,
                sortable: true,
                dataIndex: 'skill',
                field: {
                    xtype: 'combobox',
                    typeAhead : true,
                    triggerAction: 'all',
                    selectOnTab: true,
                    queryCache: false,
                    // store: [ 'C#', 'C++', 'NotARealSkill'],  // need to replace this.
                    store: Ext.create('Ext.data.Store', {
                        autoLoad: true,
                        model: 'Skill',
                        proxy:
                        {
                            type: 'rest',
                            pageParam: false, //to remove param "page"
                            startParam: false, //to remove param "start"
                            limitParam: false,
                            url: '/skills_ds/skills.json',
                            extraParams: {
                                id: 1  // This needs to be changed?
                            },
                            reader:
                            {
                                type: 'json',
                                idProperty: 'id',               //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                                messageProperty: 'message',     //# Added from a different the example in case it helps (http://www.sencha.com/forum/showthread.php?275922-REST-Store-autosyncing-empty-inserted-row)
                                root: 'data',
                                model : 'Skill'
                            },
                            writer:
                            {
                                type: 'json'
                            }
                        }
                    }),
                    emptyText: 'Select a Skill',
                    valueField : 'name',
                    displayField : 'name',
                    id : 'combo-select-skill-id',
                    lazyRender: true,
                    listClass: 'x-combo-list-medium',
                    listeners: {
                       beforeEdit: function(e) {
                           var selectedRecord = grid.getSelectionModel().getSelection()[0];
                           this.store.extraParams = {'id': selectedRecord.data.categoryID };
                           this.store.proxy.extraParams = {'id': selectedRecord.data.categoryID };
                           this.store.reload();
                       },
                       beforeQuery: function(query) {
                           var selectedRecord = grid.getSelectionModel().getSelection()[0];
                           this.store.extraParams = {'id': selectedRecord.data.categoryID };
                           this.store.proxy.extraParams = {'id': selectedRecord.data.categoryID };
                           this.store.reload();
                       }
                    }
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
