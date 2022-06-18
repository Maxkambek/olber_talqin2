import math


def calc_distance(address1, address2):
    lat1 = float(address1.split(",")[0])
    lon1 = float(address1.split(",")[1])
    lat2 = float(address2.split(",")[0])
    lon2 = float(address2.split(",")[1])
    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    return meters / 1000.0  # output distance in kilometers


from_add = "41.337217 69.284756"
to_add = "41.326756 69.282663"

lat1 = float(from_add.split()[0])
lon1 = float(from_add.split()[1])
lat2 = float(to_add.split()[0])
lon2 = float(to_add.split()[1])
# print(calc_distance(lat1, lon1, lat2, lon2))
# print(lat1, lon1, lat2, lon2)