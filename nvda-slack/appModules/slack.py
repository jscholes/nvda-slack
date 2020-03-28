import api
import appModuleHandler
import controlTypes
import ui


CLS_MSG_LIST = 'c-message_list'
CLS_MSG_TEXT = 'p-rich_text_section'


def isSlackMessage(obj):
	return 'c-message_list' in getattr(obj.simpleParent, 'IA2Attributes', {}).get('class', '')


def getSlackMessageTextContainer(obj):
	for desc in obj.recursiveDescendants:
		if CLS_MSG_TEXT in getattr(desc, 'IA2Attributes', {}).get('class', ''):
			return desc
	return None


def findLinksInMessage(msgContainer):
	links = []
	for child in msgContainer.children:
		if child.role == controlTypes.ROLE_LINK:
			links.append(child)
	return links


class AppModule(appModuleHandler.AppModule):
	def script_openURL(self, gesture):
		nav = api.getNavigatorObject()
		if not isSlackMessage(nav):
			ui.message("You don't seem to be focused on a Slack message")
			return

		txt = getSlackMessageTextContainer(nav)
		if txt is None:
			ui.message('Could not access the text of this message')
			return

		links = findLinksInMessage(txt)
		if not links:
			ui.message('No links were found in this message')
			return

		links[0].doAction()


	__gestures = {
		'kb:nvda+alt+u': 'openURL',
	}
