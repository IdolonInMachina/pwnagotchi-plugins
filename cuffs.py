import logging
import pwnagotchi.plugins as plugins


class Cuffs(plugins.Plugin):
    __author__ = 'idoloninmachina@gmail.com'
    __version__ = '0.0.2'
    __license__ = 'GPL3'
    __description__ = 'Restricts the pwnagotchi to only attack specified ap\'s'

    def __init__(self):
        logging.debug("[Cuffs] Cuffs plugin created")

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
            if ap['mac'] not in self.options['whitelist']:
                access_points.remove(ap)
                count += 1

        if (count > 0):
            logging.info(f"[Cuffs] Removed {count} unrestricted ap's")

    def on_wifi_update(self, agent, access_points):
        for ap in access_points:
            if ap['mac'] not in self.options['whitelist']:
                logging.error(
                    "[Cuffs] Cuffs is enabled, yet an unrestricted ap has made it past our filter.")
                logging.debug(f"Unrestricted AP: {ap}")

    def on_deauthentication(self, agent, access_point, client_station):
        if access_point['mac'] not in self.options['whitelist']:
            logging.error(
                "[Cuffs] Cuffs is enabled, yet an unrestricted ap has made it past our filter and has been deauthenticated.")
            logging.debug(f"Unrestricted AP: {ap}")

    def on_association(self, agent, access_point):
        if access_point['mac'] not in self.options['whitelist']:
            logging.error(
                "[Cuffs] Cuffs is enabled, yet an unrestricted ap has made it past our filter and has been assosciated.")
            logging.debug(f"Unrestricted AP: {ap}")
