
<img class="banner" src="collage-top.png"/>

# Privacy Policy for {{ config.mail_domain }} 

Welcome to `{{config.mail_domain}}`, a Canadian chatmail relay operated by a small team on a voluntary basis. See [this list](https://chatmail.at/relays) for relays in other jurisdictions.


## Summary: No personal data requested or collected 

Chatmail relays exist to transmit end-to-end encrypted messages between users. As such, this chatmail relay neither asks for nor retains personal information. 

A chatmail relay is unlike classic email servers (e.g., Hotmail/Outlook, Gmail, your ISP, etc) that collect and use personal data and can permanently store messages. A chatmail relay behaves more like Signal's servers, though chatmail doesn't know your phone number *and* it interoperates with other chatmail relays.

This chatmail relay: 

- unconditionally removes messages after {{ config.delete_mails_after }} days,

- prohibits sending/receiving unencrypted messages,

- does not store internet protocol (IP) addresses, 

- does not process IP addresses in relation to chatmail addresses.

Due to the resulting lack of personal data processing this chatmail server may not require a privacy policy.

## Processing when using chatmail services

We provide services optimized for the use of chatmail apps like [Delta Chat](https://delta.chat), [ArcaneChat](https://arcanechat.me), [etc](https://chatmail.at/clients), and we process only the data necessary for the setup and technical execution of message delivery. The purpose of this processing is to enable users to read, write, manage, delete, send, and receive chat messages. For this purpose, we operate server-side software that enables us to send and receive messages.

We process the following data and details:

- Outgoing and incoming messages (SMTP) are stored for transit on behalf of users until they can be delivered.

- Messages are stored for the recipient and made accessible via IMAP protocols, until explicitly deleted by users or after {{ config.delete_mails_after }} days, whichever is sooner.

- IMAP and SMTP protocols are password protected with unique credentials for each account.

- Users can retrieve or delete all stored messages without intervention from the operators using standard IMAP client tools.

- Users can connect to a "realtime relay service" to establish a peer-to-peer connection between users, allowing them to send and receive ephemeral messages which are never stored on the chatmail server.


### Account setup

Creating an account happens in one of two ways on our mail servers: 

- by scanning a QR invitation token with a compatible app;

- by letting a compatible app otherwise create an account and register it with the {{ config.mail_domain }} relay. 

In either case, we process the newly created email address without requiring any personally indentifiable information.

### Processing of messages

We process data to keep our relay operating optimally for the purposes of message receipt, dispatch, and abuse prevention:

- metadata necessary to process messages in transit (e.g., message headers, SMTP chatter),

- logs of messages in transit, for the purpose of debugging delivery problems and software errors.

We process data to protect the relay from excessive usage by adhering to:

- rate limits,

- storage limits,

- message size limits,

- any other limit necessary to ensure optimal function and to prevent abuse.

## Processing when using our website

When you visit this website, your web browser automatically sends information to the server on which it resides. The information is temporarily stored in a log file. The following information is collected and stored until it is automatically deleted in due course. This includes your:

- browser name and version,

- operating system name and version,

- access date and time,

- country of origin and IP address,

- requested file name or HTTP resource,

- amount of data transferred,

- access status (file transferred, file not found, etc),

- page from which the file was requested.

This website is hosted on infrastructure leased from an external internet infrastructure provider (EIIP). The personal data collected on this website is stored on the EIIP's servers. Our EIIP will process your data only to the extent necessary to fulfill its obligations to supply the infrastructure we have contracted it to. In order to ensure data protection-compliant processing, we have entered into a data processing agreement with our EIIP.

We process the aforementioned data for the following purposes:

- ensuring a reliable connection,

- ensuring system security and stability,

- other technical system administrative purposes.

By using our services, you permit us to perform the above processing as necessary to provide said services. We will not use any data processed for the purpose of drawing conclusions about your person or activity.


## Transfer of data

We do not retain any personal data. However, messages waiting to be delivered may contain personal data. Any such residual personal data will not be transferred to third parties for purposes other than those listed below:

a) you have given your express consent,

b) the disclosure is necessary for the assertion, exercise, or defence of legal claims and there is no reason to assume that you have an overriding interest worthy of protection in the non-disclosure of your data,

c) in the event that there is a legal obligation to disclose your data,

d) this is legally permissible and necessary for the processing of contractual relationships with you,

e) this is carried out by a service provider acting on our behalf and on our exclusive instructions, whom we have carefully selected and with whom we have entered into a corresponding contract on commissioned processing, which obliges our contractor, among other things to implement appropriate security measures and grants us comprehensive controls and powers.

## Rights of the data subject

Since no personal data is stored on our relay even in encrypted form, there is no need to provide information on these or possible objections. A deletion can be made directly in the app(s) you use to access our relay.

If you have any questions or concerns, please feel free to contact:

<a href="https://i.delta.chat/#0731BCC354B5982539B9EF3F7CCC3243F69EC865&a=6ajv3n8hy%40chtml.ca&n=chtml.ca%20custodian&i=4oQWjxE747gxA3TgxqaJkcuo&s=C0yzf6RHc1oeDhkOWskyNkGl"><img width=300 style="float: none;" src="qr-chat-with-{{config.mail_domain}}.png" /></a>

## Validity of this privacy policy 

This data protection declaration is valid as of April 2025. Due to the further development of our service and offers or due to changed legal or official requirements, it may become necessary to revise this data protection declaration from time to time.