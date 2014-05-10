## Project 5: separated out common utils into this module.

## Project 3:  Steve - adding relationships and navigation
## Adapted from: https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/GenericOrmBaseClass
## This is short-hand for creating a generic __repr__ (toString) method.
def modelToString(self) :
    ## changes: in the example, it was "self.c"; replaced "self.c" with an equivalent based on empirical
    ## debugging.
    atts = []
    ## This is not particularly ideal, but it will work for now.
    c = self._sa_class_manager
    for key in c.keys():
            if key in self.__dict__:

                # Steve: adding this safety check.
                keyInfo = c.get(key)
                if (hasattr(keyInfo, 'default')):

                    if not (hasattr(c.get(key).default, 'arg') and
                        getattr(c.get(key).default, 'arg') == getattr(self, key)):
                            atts.append( (key, getattr(self, key)) )

    return self.__class__.__name__ + '(' + ', '.join(x[0] + '=' + repr(x[1]) for x in atts) + ')'
