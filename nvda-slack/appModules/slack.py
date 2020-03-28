import api
import appModuleHandler
import ui


def isSlackMessage(obj):
	return 'c-message_list' in getattr(obj.simpleParent, 'IA2Attributes', {}).get('class', '')


class AppModule(appModuleHandler.AppModule):
	def script_openURL(self, gesture):
		nav = api.getNavigatorObject()
		if not isSlackMessage(nav):
			ui.message("You don't seem to be focused on a Slack message")
			return
		else:
			msg = nav
			ui.message('This is a slack message')

	__gestures = {
		'kb:nvda+alt+u': 'openURL',
	}
