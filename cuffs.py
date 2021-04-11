import logging
import pwnagotchi.plugins as plugins


class Cuffs(plugins.Plugin):
    __author__ = 'idoloninmachina@gmail.com'
    __version__ = '0.0.9'
    __license__ = 'GPL3'
    __description__ = 'Restricts the pwnagotchi to only attack specified ap\'s'

    def __init__(self):
        logging.debug("[Cuffs] Cuffs plugin created")
        self.filtered_ap_list = None

    def on_loaded(self):
        logging.info("[Cuffs] Plugin loading")

        if 'whitelist' not in self.options:
            self.options['whitelist'] = list()

        logging.info("[Cuffs] Plugin loaded")

    def on_unload(self, ui):
        logging.info("[Cuffs] Plugin unloaded")

    def on_unfiltered_ap_list(self, agent, access_points):
        count = 0
        for ap in access_points:
            # logging.info(f"[Cuffs Debug] type {type(ap)} {ap}")
            # If the ap is being restricted by cuffs, remove it
            if not self.is_whitelisted(ap):
                access_points.remove(ap)
                count += 1
        self.filtered_ap_list = access_points
        logging.info(f"[Cuffs] Removed {count} unrestricted ap's")
        logging.info(
            f"[Cuffs Debug] Filtered AP list: {[ap['mac'] for ap in access_points]}")

    def on_wifi_update(self, agent, access_points):
        agent.access_points = self.filtered_ap_list
        for ap in access_points:
            # If the app is not being whitelisted by cuffs, it should not be here
            if not self.is_whitelisted(ap):
                logging.error(
                    f"[Cuffs] Cuffs is enabled, yet an unrestricted ap ({ap['hostname']} from {ap['vendor']}) made it past our filter.")
                logging.debug(f"Unrestricted AP: {ap}")
        logging.info(
            f"[Cuffs Debug] Filtered AP list: {[ap['mac'] for ap in access_points]}")

    def on_deauthentication(self, agent, access_point, client_station):
        # If the ap is not being whitelisted by cuffs, it should not be here
        if not self.is_whitelisted(access_point):
            logging.error(
                f"[Cuffs] Cuffs is enabled, yet an unrestricted ap ({access_point['hostname']} from {access_point['vendor']})has made it past our filter and has been deauthenticated.")
            logging.debug(f"Unrestricted AP: {access_point}")

    def is_whitelisted(self, ap):
        '''
            Returns True if the ap is not being restricted by cuffs
        '''
        for whitelisted_ap in self.options['whitelist']:
            if whitelisted_ap.lower() == ap['mac'].lower() or whitelisted_ap.lower() == ap['hostname'].lower():
                return True
        return False
