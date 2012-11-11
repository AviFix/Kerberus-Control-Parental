/*++

Copyright (c) 1998  Microsoft Corporation

Module Name:

    qos.h - QoS definitions for NDIS components.

Abstract:

    This module defines the type of objects that can go into the 
    ProviderSpecific buffer in the QOS structure.

Revision History:

--*/

#ifndef __QOSSP_H_
#define __QOSSP_H_

/*
 * Definition of object Types
 *
 *
 * define the values for ObjectType above - RSVP Objects ids start at an 
 * offset from zero to allow for ATM objects that might be defined in the 
 * lower number range.
 */
#define   RSVP_OBJECT_ID_BASE         1000
#define   RSVP_OBJECT_STATUS_INFO     (0x00000000 + RSVP_OBJECT_ID_BASE)
          /* RSVP_STATUS_INFO structure passed */
#define   RSVP_OBJECT_RESERVE_INFO    (0x00000001 + RSVP_OBJECT_ID_BASE)
          /* RSVP_RESERVE_INFO structure passed */
#define   RSVP_OBJECT_ADSPEC          (0x00000002 + RSVP_OBJECT_ID_BASE)
          /* RSVP_ADSPEC structure passed */
#define   RSVP_OBJECT_POLICY_INFO    (0x00000003 + RSVP_OBJECT_ID_BASE)
          /* RSVP POLICY ELEMENT(S) retrieved */


/* 
 * IPV6 addressing for RSVP FILTERSPECS
 */
typedef union _IN_ADDR_IPV4 {

    ULONG  Addr;
    UCHAR  AddrBytes[4];

} IN_ADDR_IPV4, *LPIN_ADDR_IPV4;

/*
 * IPV6 addressing for RSVP FILTERSPECS
 */
typedef struct _IN_ADDR_IPV6 {

    UCHAR  Addr[16];               //IPV6 address

} IN_ADDR_IPV6, *LPIN_ADDR_IPV6;

typedef const IN_ADDR_IPV6  *LPCIN_ADDR_IPV6;

/*
 * IPV4 addressing for RSVP FILTERSPECS
 */
typedef struct _RSVP_FILTERSPEC_V4 {

    IN_ADDR_IPV4    Address;
    USHORT          Unused;
    USHORT          Port;

} RSVP_FILTERSPEC_V4, *LPRSVP_FILTERSPEC_V4;

typedef struct _RSVP_FILTERSPEC_V6 {

    IN_ADDR_IPV6    Address;
    USHORT          UnUsed;
    USHORT          Port;

} RSVP_FILTERSPEC_V6, *LPRSVP_FILTERSPEC_V6;


typedef struct _RSVP_FILTERSPEC_V6_FLOW {

    IN_ADDR_IPV6    Address;
    UCHAR           UnUsed;
    UCHAR           FlowLabel[3];

} RSVP_FILTERSPEC_V6_FLOW, *LPRSVP_FILTERSPEC_V6_FLOW;

typedef struct _RSVP_FILTERSPEC_V4_GPI {

    IN_ADDR_IPV4    Address;
    ULONG           GeneralPortId;

} RSVP_FILTERSPEC_V4_GPI, *LPRSVP_FILTERSPEC_V4_GPI;

typedef struct _RSVP_FILTERSPEC_V6_GPI {

    IN_ADDR_IPV6    Address;
    ULONG           GeneralPortId;

} RSVP_FILTERSPEC_V6_GPI, *LPRSVP_FILTERSPEC_V6_GPI;


/*
 * FILTERSPEC TYPES used in making reservations.
 */
typedef enum {

        FILTERSPECV4 = 1,
        FILTERSPECV6,
        FILTERSPECV6_FLOW,
        FILTERSPECV4_GPI,
        FILTERSPECV6_GPI,
        FILTERSPEC_END

} FilterType;

typedef struct _RSVP_FILTERSPEC {

    FilterType   Type;

    union {
        RSVP_FILTERSPEC_V4      FilterSpecV4;
        RSVP_FILTERSPEC_V6      FilterSpecV6;
        RSVP_FILTERSPEC_V6_FLOW FilterSpecV6Flow;
        RSVP_FILTERSPEC_V4_GPI  FilterSpecV4Gpi;
        RSVP_FILTERSPEC_V6_GPI  FilterSpecV6Gpi;
    };

} RSVP_FILTERSPEC, *LPRSVP_FILTERSPEC;

/*
 * FLOWDESCRIPTOR Structure used for specifying one or more
 * Filters per Flowspec.
 */
typedef struct _FLOWDESCRIPTOR {

    FLOWSPEC            FlowSpec;
    ULONG               NumFilters;
    LPRSVP_FILTERSPEC   FilterList;

} FLOWDESCRIPTOR, *LPFLOWDESCRIPTOR;

/*
 * RSVP_POLICY contains undefined policy data.  RSVP transports this
 * data on behalf of the Policy Control component.
 */
typedef struct _RSVP_POLICY {
    USHORT  Len;         /* total length of this element object */
    USHORT  Type;
    UCHAR   Info[4];
} RSVP_POLICY, *LPRSVP_POLICY;

typedef const RSVP_POLICY *LPCRSVP_POLICY;
#define RSVP_POLICY_HDR_LEN    ( sizeof(USHORT) + sizeof(USHORT) )

/*
 * RSVP_RESERVE_INFO Structure used for storing RSVP specific
 * information for fine tuning interaction via the Winsock2
 * Generic QoS API via the provider specific buffer. This structure
 * includes the QOS_OBJECT_HDR structure directly
 */

typedef struct _RSVP_RESERVE_INFO {

    QOS_OBJECT_HDR      ObjectHdr;            /* type and length of this object */
    ULONG               Style;                /* RSVP Style (FF,WF,SE) */
    ULONG               ConfirmRequest;       /* Non Zero for Confirm Request (receive only) */
    ULONG               NumPolicyElement;     /* Number of policy elements */
    LPRSVP_POLICY       PolicyElementList;    /* Points to the set of policy elements */
    ULONG               NumFlowDesc;          /* Number of FlowDesc */
    LPFLOWDESCRIPTOR    FlowDescList;         /* Points to the FlowDesc list */

} RSVP_RESERVE_INFO, *LPRSVP_RESERVE_INFO;

typedef const RSVP_RESERVE_INFO *LPCRSVP_RESERVE_INFO;

/*
 * definitions for the ulStyle in the previous structure
 */
#define RSVP_DEFAULT_STYLE            0x00000000
#define RSVP_WILDCARD_STYLE           0x00000001
#define RSVP_FIXED_FILTER_STYLE       0x00000002
#define RSVP_SHARED_EXPLICIT_STYLE    0x00000003

/*
 * RSVP_STATUS_INFO Structure used for storing RSVP specific
 * error of status indications.  This also serves as a header
 * for additional objects in the provider specific buffer when
 * interacting via Winsock2 Generic QoS API. This structure includes
 * the QOS_OBJECT_COUNT and QOS_OBJECT_HDR structures directly It is
 * expected to be the first structure in the provider specific structure
 * since it includes the QOS_OBJECT_COUNT
 */

typedef struct _RSVP_STATUS_INFO {

    QOS_OBJECT_HDR      ObjectHdr;      /* Object Hdr */
    ULONG               StatusCode;     /* Error or Status Information see 
                                         * Winsock2.h */
    ULONG               ExtendedStatus1;/* Provider specific status extension */
    ULONG               ExtendedStatus2;/* Provider specific status extension */

} RSVP_STATUS_INFO, *LPRSVP_STATUS_INFO;

typedef const RSVP_STATUS_INFO *LPCRSVP_STATUS_INFO;


/*
 * QOS_DestAddr structure -- used for WSAIoctl(SIO_SET_QOS) when we
 * do not want to issue a connect for a sending socket.  The destination
 * address is required so we can generate the session information for
 * RSVP signalling.
*/

typedef struct _QOS_DESTADDR {
    QOS_OBJECT_HDR ObjectHdr;                     /* Object header */
    const struct sockaddr *  SocketAddress;       /* Destination socket address */
    ULONG                    SocketAddressLength; /* Length of the address structure */
} QOS_DESTADDR, *LPQOS_DESTADDR;

typedef const QOS_DESTADDR * LPCQOS_DESTADDR;



/*
 * this structure defines the "General Characterization Parameters" contained in
 * the RSVP Adspec object
 */
typedef struct _AD_GENERAL_PARAMS{

    ULONG       IntServAwareHopCount;   /* number of hops that conform to
                                         * Integrated Services requirements */
    ULONG       PathBandwidthEstimate;  /* minimum bandwidth available from 
                                         * sender to receiver */
    ULONG       MinimumLatency;         /* sum of minimum latency of the packet
                                         * forwarding process in routers 
                                         * (in usec)*/
    ULONG       PathMTU;                /* max transmission unit end to end that
                                         * will not incur fragmentation */
    ULONG       Flags;                  /* used to hold break bits.*/

} AD_GENERAL_PARAMS, *LPAD_GENERAL_PARAMS;

/*
 * Minimum Latency may be set to this "undefined" value
 */
#define INDETERMINATE_LATENCY   0xFFFFFFFF;

/*
 * This Flag is used to indicate the existence of a network element not 
 * supporting  QoS control services somewhere in the data path. If this bit 
 * is set in the specific service override then it indicates that that
 * service was not supported at at least one hop.
 */
#define AD_FLAG_BREAK_BIT    0x00000001

/*
 * this structure describes the Guaranteed service parameters
 */
typedef struct _AD_GUARANTEED {

    ULONG       CTotal;
    ULONG       DTotal;
    ULONG       CSum;
    ULONG       DSum;

} AD_GUARANTEED, *LPAD_GUARANTEED;

/*
 * this structure describes the format of the parameter buffer that can be
 * included in the Service_Type structure below.  This structure allows an
 * application to include any valid Int Serv service parameter in the Buffer 
 * value, after providing the Int Serv parameter id in the ParameterId field.
 */
typedef struct _PARAM_BUFFER {

    ULONG   ParameterId;    /* Int Server parameter ID */
    ULONG   Length;         /* total length of this structure 
                             * ( 8 bytes + length of Buffer ) */
    UCHAR   Buffer[1];      /* Paramter itself */

} PARAM_BUFFER, *LPPARAM_BUFFER;

/*
 * this structure contains the service types supported
 */
typedef struct _CONTROL_SERVICE {

    /*
     * the length of this entire structure including the following buffer.  
     * This length value can be added to the ptr to the structure to get the ptr
     * to the next SERVICE_TYPE structure in the list, until the
     * NumberOfServices count has been exhausted.
     */
    ULONG               Length;

    SERVICETYPE         Service;
    AD_GENERAL_PARAMS   Overrides;

    /*
     * service specific information ( controlled load has no service specific 
     * info here )
     */
    union {
        AD_GUARANTEED   Guaranteed;
        PARAM_BUFFER    ParamBuffer[1];     /* allows for other services down 
                                             * the road */
    };

} CONTROL_SERVICE, *LPCONTROL_SERVICE;

/*
 * This structure defines the information which is carried in the Rsvp 
 * Adspec.  This Rsvp object typically indicates which service types are 
 * available ( Controlled Load and/or Guaranteed Service ), if a non-Rsvp
 * hop has been encountered by the Path message, and the minumum MTU along 
 * the path. The services array indicates which services are supported
 */
typedef struct _RSVP_ADSPEC  {

    QOS_OBJECT_HDR     ObjectHdr;
    AD_GENERAL_PARAMS  GeneralParams;      /* contains the general 
                                            * characterization paramters */
    ULONG              NumberOfServices;   /* count of the number of services */
    CONTROL_SERVICE    Services[1];        /* a list of the services 
                                            * supported/requested */

} RSVP_ADSPEC, *LPRSVP_ADSPEC;

/*
 * RSVP_POLICY_INFO contains undefined policy element(s) retrieved from RSVP.  
 */
typedef struct _RSVP_POLICY_INFO  {

    QOS_OBJECT_HDR     ObjectHdr;
    ULONG              NumPolicyElement;         /* count of the 
                                                  * number of policy elements */
    RSVP_POLICY        PolicyElement[1];         /* a list of the policy 
                                                  * elements retrieved */

} RSVP_POLICY_INFO, *LPRSVP_POLICY_INFO;


//
// Opcode for the SIO_CHK_QOS ioctl
// (specific for the Microsoft QOS Service Provider
//
// Bascially:
//
// SIO_CHK_QOS = _WSAIORW(IOC_VENDOR,1)
//             = mIOC_IN | mIOC_OUT | mIOC_VENDOR | mCOMPANY | ioctl_code
//    where
//         mIOC_IN     = 0x80000000
//         mIOC_OUT    = 0x40000000
//         mIOC_VENDOR = 0x04000000
//         mCOMPANY    = 0x18000000
//         ioctl_code  = 0x00000001
//         
// See WSAIoctl man page for details.
//

#define    mIOC_IN       0x80000000
#define    mIOC_OUT      0x40000000
#define    mIOC_VENDOR   0x04000000
#define    mCOMPANY      0x18000000
#define    ioctl_code    0x00000001

#define SIO_CHK_QOS   mIOC_IN | mIOC_OUT | mIOC_VENDOR | mCOMPANY | ioctl_code

//
// The following may be specified in the input buffer 
// of the SIO_CHK_IOCTL ioctl call 
//

#define QOSSPBASE           50000

#define ALLOWED_TO_SEND_DATA (QOSSPBASE+1)      // query the SBM/BEST_EFFORT limit 
                                                //   -- result is based on a comparison between
                                                //      the user-specified token rate and the
                                                //      SBM/BEST_EFFORT bandwidth parameters in
                                                //      the system
                                                //   -- result is a YES(1) or NO(0) answer
                                                //      in the output buffer 

#define ABLE_TO_RECV_RSVP   (QOSSPBASE+2)       // query the SBM/BEST_EFFORT limit 
                                                //   -- result is based on a comparison between
                                                //      the user-specified token rate and the
                                                //      SBM/BEST_EFFORT bandwidth parameters in
                                                //      the system
                                                //   -- result is a YES(1) or NO(0) answer
                                                //      in the output buffer 

#define LINE_RATE           (QOSSPBASE+3)       // query the interface capacity 
                                                //   -- result returned in the output buffer
                                                //      in kilo-bits per second

#define INFO_NOT_AVAILABLE  0xFFFFFFFF          // used when LINE_RATE is not known


#define QUERY_PS_SIZE       0xFFFFFFFF          // used in SIO_GET_QOS to query the
                                                // required buffer size

#endif  /* __QOSSP_H_ */

