# PG artifact manifest BR_Com_004

Danh sách file PG và build/lint config đã review G1. Path tuyệt đối hoặc tương đối từ task.
Role ghi rõ production-code hoặc build-config.
Không yêu cầu UT code tại G1. Danh sách PG/UT cuối nằm trong artifact-manifest.md ở S6.
File thiếu chặn kiểm tra. User tự commit; SHA ghi nếu có.

Code commit: không bắt buộc (user tự commit trên branch `bd-to-pg`).

## Files

| ID | Path | Role |
|---|---|---|
| F-01 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Models\Room.cs | production-code (new) |
| F-02 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Models\Tablet.cs | production-code (new) |
| F-03 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Models\CandidateRoom.cs | production-code (new) |
| F-04 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Repositories\IRoomRepository.cs | production-code (new) |
| F-05 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Repositories\ITabletRepository.cs | production-code (new) |
| F-06 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\RasDbContext.cs | production-code (modified, shared) |
| F-07 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\EntityConfigurations\RoomEntityTypeConfiguration.cs | production-code (new) |
| F-08 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\EntityConfigurations\TabletEntityTypeConfiguration.cs | production-code (new) |
| F-09 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\EntityConfigurations\CandidateRoomEntityTypeConfiguration.cs | production-code (new) |
| F-10 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\Repositories\RoomRepository.cs | production-code (new) |
| F-11 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\Repositories\TabletRepository.cs | production-code (new) |
| F-12 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\ViewModels\RoomsMstOutput.cs | production-code (new) |
| F-12a | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\ViewModels\CandidateRoomOutput.cs | production-code (new) |
| F-12b | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\ViewModels\TabletInfoOutput.cs | production-code (new) |
| F-12c | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\ViewModels\SaveTabletInfoInput.cs | production-code (new) |
| F-13 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\Services\ITabletInfoService.cs | production-code (new) |
| F-14 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\Services\TabletInfoService.cs | production-code (new) |
| F-15 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\ViewModels\SaveTabletInfoRequest.cs | production-code (new) |
| F-15a | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\ViewModels\RoomsMstListRequest.cs | production-code (new) |
| F-15b | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\ViewModels\RoomsMstResponse.cs | production-code (new) |
| F-15c | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\ViewModels\CandidateRoomResponse.cs | production-code (new) |
| F-15d | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\ViewModels\TabletInfoResponse.cs | production-code (new) |
| F-15e | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Mapper\TabletInfoProfile.cs | production-code (new: AutoMapper Profile) |
| F-16 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Controllers\TabletInfoController.cs | production-code (new) |
| F-17 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Controllers\RoomsController.cs | production-code (new) |
| F-18 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Startup.cs | production-code (modified, shared: DI) |
| F-19 | D:\Serio-AI\serio-ras\ras-system\src\BuildingBlocks\Common\Util\Resources\Messages.resx | production-code (modified, shared: message E_BRCOM004_001) |
| F-20 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-004\components\br-com-004.component.ts | production-code (new) |
| F-21 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-004\components\br-com-004.component.html | production-code (new) |
| F-22 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-004\components\br-com-004.component.css | production-code (new) |
| F-23 | D:\Serio-AI\serio-ras\ras-web\src\app\shared\services\rooms-mst.service.ts | production-code (new, shared service API_008) |
| F-23a | D:\Serio-AI\serio-ras\ras-web\src\app\shared\services\tablet-info.service.ts | production-code (new, shared service API_004/005) |
| F-24 | D:\Serio-AI\serio-ras\ras-web\src\app\shared\interfaces\rooms-mst-response.interface.ts | production-code (new, shared interface) |
| F-24a | D:\Serio-AI\serio-ras\ras-web\src\app\shared\interfaces\candidate-room-response.interface.ts | production-code (new, shared interface) |
| F-24b | D:\Serio-AI\serio-ras\ras-web\src\app\shared\interfaces\tablet-info-response.interface.ts | production-code (new, shared interface) |
| F-24c | D:\Serio-AI\serio-ras\ras-web\src\app\shared\interfaces\save-tablet-info-request.interface.ts | production-code (new, shared interface) |
| F-24d | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-004\interfaces\candidate-room-view-model.interface.ts | production-code (new) |
| F-25 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-003\components\br-com-003-mock.component.ts | production-code (new, mock BR_Com_003) |
| F-26 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-003\components\br-com-003-mock.component.html | production-code (new, mock BR_Com_003) |
| F-27 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-003\components\br-com-003-mock.component.css | production-code (new, mock BR_Com_003) |
| F-28 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-003\interfaces\room-search-input.interface.ts | production-code (new, mock BR_Com_003 contract) |
| F-28a | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-003\interfaces\room-search-result-item.interface.ts | production-code (new, mock BR_Com_003 contract) |
| F-29 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-005\components\br-com-005-mock.component.ts | production-code (new, mock BR_Com_005) |
| F-30 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-005\components\br-com-005-mock.component.html | production-code (new, mock BR_Com_005) |
| F-31 | D:\Serio-AI\serio-ras\ras-web\src\app\features\br-com-005\components\br-com-005-mock.component.css | production-code (new, mock BR_Com_005) |
| F-32 | D:\Serio-AI\serio-ras\ras-web\src\app\app.routes.ts | production-code (modified, shared: routes BrCom004, error/:statusCode) |
| F-32a | D:\Serio-AI\serio-ras\ras-web\src\app\shared\components\app-shell-layout\app-shell-layout.component.ts | production-code (modified, shared: menu route 'BRCom004' → 'BrCom004') |
| F-33 | D:\Serio-AI\serio-ras\ras-web\src\app\shared\guards\admin.guard.ts | production-code (modified, shared: redirect → /error/403) |
| F-34 | D:\Serio-AI\serio-ras\ras-web\src\app\shared\services\api-error-handler.service.ts | production-code (modified, shared: redirect → /error/{status}) |
| F-35 | D:\Serio-AI\serio-ras\ras-web\src\assets\i18n\ja.json | production-code (modified, shared: i18n keys) |
| F-38 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Infrastructure\Authorization\AuthorizationPolicySetup.cs | production-code (new, review 2.4: policy role) |
| F-39 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Shared\Constants\AppRoles.cs | production-code (modified, shared: InternalUser) |
| F-40 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Shared\Constants\AuthorizationPolicies.cs | production-code (modified, shared: InternalUserOrAdministrator) |
| F-41 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi.ComponentTests\Authorization\ApiRoleAuthorizationTests.cs | test-code (new, review 2.4: 401/403 API_004/005/008) |
| F-42 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi.ComponentTests\Mapper\TabletInfoProfileTests.cs | test-code (new: AutoMapper Profile) |
| F-36 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\RasApi.csproj | build-config (không sửa; lệnh build) |
| F-37 | D:\Serio-AI\serio-ras\ras-web\angular.json | build-config (không sửa; budget production có sẵn đang vượt) |

Đã xóa khi refactor theo コーディング規約/PG_ルール (2026-10-19): `TabletInfoModels.cs`, `TabletInfoRequests.cs`, thư mục `features/tablet-registration`, `features/room-search-mock`, `features/error-mock`.
