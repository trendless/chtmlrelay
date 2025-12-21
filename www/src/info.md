
<!--img class="banner" src="collage-top.png"/-->


{{ config.mail_domain }} provides a low-maintenance, resource-efficient, interoperable, and end-to-end encrypted messaging relay. A `chatmail` account is a standard email address that's configured and optimized for verifiably secure instant messaging.


### Rate and storage limits 

- Unencrypted messages are blocked to recipients outside {{config.mail_domain}}. You can add other chatmail users by sharing [QR invite codes](https://delta.chat/en/help#howtoe2ee), which create an encrypted connection between you and them so messages can be sent and received securely.

- You may send up to {{ config.max_user_send_per_minute }} messages per minute.

- The relay will allow you to temporarily cache up to [{{ config.max_mailbox_size }}iB of messages](https://delta.chat/en/help#what-happens-if-i-turn-on-delete-old-messages-from-server).

- Messages are unconditionally removed a maximum of {{ config.delete_mails_after }} days after arriving on the relay.


### <a name="account-deletion"></a> Account deletion 

{{ config.mail_domain }} accounts and any temporarily cached messages contained therein are automatically deleted after {{ config.delete_inactive_users_after }} days of no login activity. 

If you wish to delete your account, you must remove it from ***all*** of the apps/devices on which it's setup.

Deleted accounts ***cannot*** be restored.

If you have any further questions, please send a message from your chatmail account to:

<div class="qr-container">
<a class="cta-button" href="https://i.delta.chat/#437A67FC59E76D0632027DBB1A2B1CD87C67C1A5&i=FwGoQ8l55W_OljDGoPJK7kup&s=pCuREcbpjPbJF-bIGqqP0sF0&a=1tjaykajl%40chatma.li&n=chatma.li">chatma.li</a>
<input type="checkbox" id="qrToggle2" class="qr-toggle">
<label for="qrToggle2"> <img src="qr_code.png" alt="qr thumbnail" class="qr-thumb"> </label>
<div class="qr-panel"> <img src="qr-chatmali-invite.png" alt="chatma.li invite qr code"></div>
</div>

### What's running under the hood? 

{{config.mail_domain}} employs free, open-source software assembled by a small group of voluntary devs who publicly develop the reference chatmail relay implementation -- which aims to be low-maintenance, resource-efficient, and interoperable with other standards-compliant encrypted email services. 
