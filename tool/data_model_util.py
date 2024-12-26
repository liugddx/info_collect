import pysmartdatamodels as sdm

def open_jsonref(fileUrl: str):
    import requests
    import jsonref
    """
    Opens a JSON file given its URL or path and returns the loaded content as a JSON object.
    Capable of parsing JSON file with $ref
    Parameters:
    - file_url (str): The URL or path of the JSON file.
    Returns:
    - dict: The loaded JSON content if successful, none otherwise.
    Example:
    open_jsonref("https://example.com/data.json")
    {...}
    open_jsonref("local_file.json")
    {...}
    open_jsonref("invalid-url")
    None
    """
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True, merge_props=True)
            return output
        except:
            return None
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return jsonref.loads(file.read(), load_on_repr=True, merge_props=True)
        except:
            return None


#主题
subject = "dataModel.Weather"

#模型
dataModel = "WeatherForecast"

attribute = "precipitation"

serverUrl = "https://smartdatamodels.org:1026"

value = 0.5

schemaUrl = "https://smart-data-models.github.io/dataModel.Agrifood/AgriApp/schema.json"

modelYaml = "https://raw.githubusercontent.com/smart-data-models/dataModel.Transportation/master/FareCollectionSystem/model.yaml"

DCATAPExampleUrl = "example.json"

content_DCAT = open_jsonref(DCATAPExampleUrl)


# Load all datamodels in a dict like the official list
print("1 : ")
print(sdm.load_all_datamodels())

# Load all attributes in a dict like the official export of attributes
print("2 : ")
print(len(sdm.load_all_attributes()))   # there is more than 155.000 to get all listed

# List all data models
print("3 : ")
print(sdm.list_all_datamodels())

# List all subjects
print("4 : ")
print(sdm.list_all_subjects())

# List the data models of a subject
print("5 : ")
print(sdm.datamodels_subject("dataModel.Weather"))

# List description of an attribute
print("6 : ")
print(sdm.description_attribute(subject, dataModel, attribute))

# List data-type of an attribute
print("7 : ")
print(sdm.datatype_attribute(subject, dataModel, attribute))

# Give reference model for an attribute
print("8 : ")
print(sdm.model_attribute(subject, dataModel, attribute))

# Give reference units for an attribute
print("9 : ")
print(sdm.units_attribute(subject, dataModel, attribute))

# List the attributes of a data model
print("10 : ")
print(sdm.attributes_datamodel(subject, dataModel))

# List the NGSI type (Property, Relationship or Geoproperty) of the attribute
print("11 : ")
print(sdm.ngsi_datatype_attribute(subject, dataModel, attribute))

# Validate a json schema defining a data model
print("12 : ")
print(sdm.validate_data_model_schema(schemaUrl))

# Print a list of data models attributes separated by a separator
print("13 : ")
print(sdm.print_datamodel(subject, dataModel, ",", [
        "property",
        "type",
        "dataModel",
        "repoName",
        "description",
        "typeNGSI",
        "modelTags",
        "format",
        "units",
        "model",
    ]))

# Returns the link to the repository of a subject
print("14 : ")
print(sdm.subject_repolink(subject))

# Return the links to the repositories of a data model name
print("15 : ")
print(sdm.datamodel_repolink(dataModel))

# Update the official data model list or the database of attributes from the source
# It will take a while
print("16 : ")
sdm.update_data()

# Return a fake normalized ngsi-ld format example based on the given json schema
print("17 : ")
print(sdm.ngsi_ld_example_generator(schemaUrl))

# Return a fake key value ngsi-ld format example based on the given json schema
print("18 : ")
print(sdm.ngsi_ld_keyvalue_example_generator(schemaUrl))

# Return a fake geojson feature format example based on the given json schema
print("19 : ")
print(sdm.geojson_features_example_generator(schemaUrl))

# Update a broker compliant with a specific data model, inspired by Antonio Jara
print("20 : ")
print(sdm.update_broker(dataModel, subject, attribute, value, serverUrl=serverUrl, updateThenCreate=True))

# Generate a SQL export based on the model.yaml (yaml export of the schema of a data model)
print("21 : ")
print(sdm.generate_sql_schema(modelYaml))

# Look for a data model name
print("22 : ")
print(sdm.look_for_datamodel("WeatherFora", 84))

# retrieve the metadata, context, version, model tags, schema, yaml schema, title, description, $id, required, examples, adopters, contributors and sql export of a data model
print("23 : ")
print(sdm.list_datamodel_metadata(dataModel, subject))

# retrieve the metadata, context, version, model tags, schema, yaml schema, title, description, $id, required, examples, adopters, contributors and sql export of a data model
print("23 : ")
print(sdm.list_datamodel_metadata(dataModel, subject))

print("24:")
print(sdm.validate_dcat_ap_distribution_sdm(content_DCAT))

print("25:")
print(sdm.subject_for_datamodel(dataModel))