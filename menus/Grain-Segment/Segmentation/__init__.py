class Transfer:
    """Storage class for exchanging variables.
       ...

    """

    def attributes(self):
        """Prints currently contained data members."""
        print('Currently the following attributes are available: ', list(vars(self).keys()))


storage = Transfer()

catlog = ['Workflow', 'Demos', 'Help', '-']
