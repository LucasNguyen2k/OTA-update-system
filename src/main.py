from src.ota_package import OTAPackage
from src.verifier import Verifier
from src.updater import Updater
from src.vehicle import Vehicle

if __name__ == "__main__":

    # Create a vehicle instance
    vehicle = Vehicle("vehicle_001", "1.0.0")
    
    # Create an update package
    files = [
        {"path": "ecu_software.bin", "hash": "367d4a22a38905d54db64880558bc5c62884d006c431b7e4061bb36b3f97d224", "size": 1049}
    ]
    package = OTAPackage("my-package", "1.1.0", files)

    # Set up verifier and updater
    verifier = Verifier("public_key.pem")
    updater = Updater(verifier)

    # Apply update
    success = updater.apply_update(package, package.package_id)

    if success:
        vehicle.record_update(package.package_id, package.version, "2024-01-01")

    print(f"Update applied: {success}")
    
    print(f"Vehicle update history: {vehicle.update_history}")
    """
    print(f"Vehicle current version: {vehicle.current_version}")    
    print(f"Vehicle installed components: {vehicle.installed_components}")
    print(f"Vehicle state: {vehicle.to_dict()}")
    print(f"Package manifest: {package.to_manifest()}")
    print(f"Package ID: {package.package_id}, Version: {package.version}")
    """ 