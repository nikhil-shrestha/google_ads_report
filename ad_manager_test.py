from googleads import ad_manager

# Initialize a client object, by default uses the credentials in ~/googleads.yaml.
ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage()

# Initialize a service.
network_service = ad_manager_client.GetService('NetworkService')

# Make a request.
current_network = network_service.getCurrentNetwork()

print('Found network %s (%s)!' % (current_network['displayName'],
                              current_network['networkCode']))