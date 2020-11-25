# Write GDX file



def fct_write_gdx_sets(lst_sets, val_path_output=None):

    # Import packages
    import gdxpds

    # Import files
    import H2forEU_sets_and_parameters
    import H2forEU_settings


    with gdxpds.gdx.GdxFile() as gdx:

        # val_path_output = None
        # lst_sets = ['set_link_hour_year']

        for i_set in lst_sets:
            print(i_set)

            function = getattr(H2forEU_sets_and_parameters, i_set)
            [gdx_name, gdx_dimension, gdx_data] = function()

            gdx.append(gdxpds.gdx.GdxSymbol(gdx_name, gdxpds.gdx.GamsDataType.Set, dims=gdx_dimension))
            gdx_data['VALUE'] = 'True'
            gdx[-1].dataframe = gdx_data
            # Create GDX file including all sets
            if val_path_output == None:
                val_path_output = H2forEU_settings.val_path_gdx_output

            gdx.write(str(val_path_output) + '//' + 'sets.gdx')

def fct_write_gdx_sets_individually(lst_sets, val_path_output=None):

    # Import packages
    import gdxpds

    # Import files
    import H2forEU_sets_and_parameters
    import H2forEU_settings

    for i_set in lst_sets:
        print(i_set)

        with gdxpds.gdx.GdxFile() as gdx:

            # val_path_output = None
            # lst_sets = ['set_link_hour_year']

            function = getattr(H2forEU_sets_and_parameters, i_set)
            [gdx_name, gdx_dimension, gdx_data] = function()

            gdx.append(gdxpds.gdx.GdxSymbol(gdx_name, gdxpds.gdx.GamsDataType.Set, dims=gdx_dimension))
            gdx_data['VALUE'] = 'True'
            gdx[-1].dataframe = gdx_data
            # Create GDX file including all sets
            if val_path_output == None:
                val_path_output = H2forEU_settings.val_path_gdx_output

            gdx.write(str(val_path_output) + '//' + i_set+'.gdx')



def fct_write_gdx_parameters(lst_parameters, val_path_output=None):

    # Import packages
    import gdxpds

    # Import files
    import H2forEU_sets_and_parameters
    import H2forEU_settings

    #with gdxpds.gdx.GdxFile() as gdx:

    for i_parameter in lst_parameters:
        print(i_parameter)

        with gdxpds.gdx.GdxFile() as gdx:

            function = getattr(H2forEU_sets_and_parameters, i_parameter)
            [gdx_name, gdx_dimension, gdx_data] = function()

            gdx.append(gdxpds.gdx.GdxSymbol(gdx_name, gdxpds.gdx.GamsDataType.Parameter, dims=gdx_dimension))
            #gdx_data = gdx_data.iloc[:,:-1]
            gdx_data = gdx_data.iloc[:,:]
            gdx[-1].dataframe = gdx_data

            # Create GDX file including all parameters
            if  val_path_output == None:
                val_path_output = H2forEU_settings.val_path_gdx_output

            gdx.write(str(val_path_output) + '//' + gdx_name + '.gdx')


def fct_write_gdx_single_parameter(gdx_name, df, lst_columns, val_path_output):

    # Import packages
    import gdxpds

    # Import files

    with gdxpds.gdx.GdxFile() as gdx:

        gdx_data = df.copy()
        gdx_data.columns = lst_columns
        gdx_dimension = gdx_data.columns[: -1].tolist()

        gdx.append(gdxpds.gdx.GdxSymbol(gdx_name, gdxpds.gdx.GamsDataType.Parameter, dims=gdx_dimension))
        #gdx_data = gdx_data.iloc[:,:-1]
        gdx_data = gdx_data.iloc[:,:]
        gdx[-1].dataframe = gdx_data

        gdx.write(str(val_path_output) + '//' + gdx_name + '.gdx')


def fct_write_gdx_single_set(gdx_name, df, lst_columns,  val_path_output):

    # Import packages
    import gdxpds

    # Import files

    with gdxpds.gdx.GdxFile() as gdx:

        df_gdx = df.copy()
        df_gdx.columns = lst_columns

        gdx_dimension = df_gdx.columns.tolist()
        gdx_data = df_gdx

        gdx.append(gdxpds.gdx.GdxSymbol(gdx_name, gdxpds.gdx.GamsDataType.Set, dims=gdx_dimension))
        gdx_data['VALUE'] = 'True'
        gdx[-1].dataframe = gdx_data
        # Create GDX file
        gdx.write(str(val_path_output) + '//' + gdx_name + '.gdx')

